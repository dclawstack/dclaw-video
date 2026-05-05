import asyncio
import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery_app import celery_app
from app.core.db import AsyncSessionLocal
from app.core.config import settings
from app.models.project import Project
from app.models.scene import Scene
from app.models.render_job import RenderJob
from app.models.storyboard import Storyboard
from app.services.comfyui_client import ComfyUIClient
from app.services.tts_service import TTSService
from app.services.video_assembler import VideoAssembler

logger = logging.getLogger(__name__)


def _get_db() -> AsyncSession:
    return AsyncSessionLocal()


async def _update_job_progress(job_id: str, percent: int, logs: str = "") -> None:
    async with _get_db() as db:
        result = await db.execute(select(RenderJob).where(RenderJob.celery_task_id == job_id))
        job = result.scalar_one_or_none()
        if job:
            job.progress_percent = percent
            if logs:
                job.logs = (job.logs or "") + logs + "\n"
            await db.commit()


async def _update_project_status(project_id: str, status: str) -> None:
    async with _get_db() as db:
        result = await db.execute(select(Project).where(Project.id == UUID(project_id)))
        project = result.scalar_one_or_none()
        if project:
            project.status = status
            await db.commit()


@celery_app.task(bind=True, name="tasks.generate_storyboard")
def generate_storyboard(self, project_id: str) -> dict:
    async def _run():
        await _update_job_progress(self.request.id, 0, "Starting storyboard generation...")
        async with _get_db() as db:
            result = await db.execute(
                select(Scene).where(Scene.project_id == UUID(project_id)).order_by(Scene.scene_number)
            )
            scenes = list(result.scalars().all())

            comfy = ComfyUIClient()
            total = len(scenes)
            for idx, scene in enumerate(scenes):
                # Generate a storyboard frame for each scene
                prompt = scene.visual_prompt or scene.narration_text[:200]
                workflow = comfy.build_flux_workflow(prompt)
                prompt_id = await comfy.queue_prompt(workflow)

                # In a real implementation, poll ComfyUI history for the result
                # For now, store a placeholder
                frame = Storyboard(
                    scene_id=scene.id,
                    frame_number=1,
                    image_url=f"comfyui://{prompt_id}/frame_1.png",
                    prompt_used=prompt,
                    selected=True,
                )
                db.add(frame)
                await db.commit()

                percent = int((idx + 1) / total * 100)
                await _update_job_progress(self.request.id, percent, f"Scene {idx+1}/{total} storyboard done")

        await _update_project_status(project_id, "storyboard")
        return {"project_id": project_id, "status": "done"}

    return asyncio.run(_run())


@celery_app.task(bind=True, name="tasks.render_scene")
def render_scene(self, scene_id: str) -> dict:
    async def _run():
        await _update_job_progress(self.request.id, 0, f"Starting scene render {scene_id}")
        async with _get_db() as db:
            result = await db.execute(select(Scene).where(Scene.id == UUID(scene_id)))
            scene = result.scalar_one_or_none()
            if not scene:
                raise ValueError(f"Scene {scene_id} not found")

            scene.status = "generating"
            await db.commit()

            # Generate TTS audio
            tts = TTSService()
            audio_bytes = tts.synthesize(scene.narration_text)

            # Generate video via ComfyUI (AnimateDiff)
            comfy = ComfyUIClient()
            workflow = comfy.build_animatediff_workflow(scene.visual_prompt or scene.narration_text)
            prompt_id = await comfy.queue_prompt(workflow)

            # Placeholder: in production, poll history and download output
            scene.video_clip_url = f"comfyui://{prompt_id}/scene.mp4"
            scene.status = "done"
            await db.commit()

        await _update_job_progress(self.request.id, 100, f"Scene {scene_id} rendered")
        return {"scene_id": scene_id, "status": "done"}

    return asyncio.run(_run())


@celery_app.task(bind=True, name="tasks.render_project")
def render_project(self, project_id: str) -> dict:
    async def _run():
        await _update_job_progress(self.request.id, 0, "Starting full project render...")
        async with _get_db() as db:
            result = await db.execute(
                select(Scene).where(Scene.project_id == UUID(project_id)).order_by(Scene.scene_number)
            )
            scenes = list(result.scalars().all())

            assembler = VideoAssembler()
            total = len(scenes)
            video_paths = []
            audio_paths = []

            for idx, scene in enumerate(scenes):
                if scene.status != "done" or not scene.video_clip_url:
                    # Auto-render missing scenes
                    scene.status = "generating"
                    await db.commit()
                    tts = TTSService()
                    audio_bytes = tts.synthesize(scene.narration_text)
                    audio_path = assembler.write_audio(str(scene.id), audio_bytes)
                    audio_paths.append(audio_path)

                    comfy = ComfyUIClient()
                    workflow = comfy.build_animatediff_workflow(scene.visual_prompt or scene.narration_text)
                    prompt_id = await comfy.queue_prompt(workflow)
                    scene.video_clip_url = f"comfyui://{prompt_id}/scene.mp4"
                    scene.status = "done"
                    await db.commit()

                video_paths.append(assembler.write_video(str(scene.id), b""))  # placeholder bytes
                percent = int((idx + 1) / total * 50)
                await _update_job_progress(self.request.id, percent, f"Scene {idx+1}/{total} ready")

            # Assemble final video
            final_path = f"/tmp/dclaw_{project_id}_final.mp4"
            # assembler.crossfade_concat(video_paths, final_path)
            # assembler.burn_subtitles(final_path, srt_path, final_burned)
            # In a real implementation, upload to MinIO and store URL

            project = await db.get(Project, UUID(project_id))
            if project:
                project.status = "done"
                project.video_url = f"minio://{settings.minio_bucket}/renders/{project_id}.mp4"
                await db.commit()

        await _update_job_progress(self.request.id, 100, "Render complete")
        return {"project_id": project_id, "status": "done", "video_url": project.video_url if project else None}

    return asyncio.run(_run())
