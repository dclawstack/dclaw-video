import os
import subprocess
import tempfile
from pathlib import Path

from app.core.config import settings


class VideoAssembler:
    def __init__(self, work_dir: str | None = None):
        self.work_dir = work_dir or tempfile.mkdtemp(prefix="dclaw_")
        Path(self.work_dir).mkdir(parents=True, exist_ok=True)

    def write_audio(self, scene_id: str, audio_bytes: bytes) -> str:
        path = os.path.join(self.work_dir, f"{scene_id}.wav")
        with open(path, "wb") as f:
            f.write(audio_bytes)
        return path

    def write_video(self, scene_id: str, video_bytes: bytes) -> str:
        path = os.path.join(self.work_dir, f"{scene_id}.mp4")
        with open(path, "wb") as f:
            f.write(video_bytes)
        return path

    def burn_subtitles(self, video_path: str, srt_path: str, output_path: str) -> str:
        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'",
            "-c:a", "copy",
            output_path,
        ]
        subprocess.run(cmd, check=True)
        return output_path

    def crossfade_concat(self, video_paths: list[str], output_path: str, fade_duration: float = 0.5) -> str:
        if len(video_paths) == 1:
            import shutil
            shutil.copy(video_paths[0], output_path)
            return output_path

        # Build FFmpeg complex filter for crossfade concatenation
        inputs = []
        for path in video_paths:
            inputs.extend(["-i", path])

        n = len(video_paths)
        filters = []
        for i in range(n - 1):
            if i == 0:
                filters.append(f"[0:v][1:v]xfade=transition=fade:duration={fade_duration}:offset=0[fade0]")
            else:
                filters.append(f"[fade{i-1}][{i+1}:v]xfade=transition=fade:duration={fade_duration}:offset=0[fade{i}]")

        final_label = f"fade{n-2}" if n > 1 else "0:v"
        filters.append(f"{final_label}format=yuv420p[outv]")

        # Audio concat
        audio_filter = ""
        for i in range(n):
            audio_filter += f"[{i}:a]"
        audio_filter += f"concat=n={n}:v=0:a=1[outa]"

        filter_complex = ";".join(filters + [audio_filter])

        cmd = [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "[outa]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path,
        ]
        subprocess.run(cmd, check=True)
        return output_path

    def generate_srt(self, scenes: list[dict], output_path: str) -> str:
        lines = []
        current_time = 0.0
        for idx, scene in enumerate(scenes, start=1):
            duration = scene.get("duration_seconds", 5.0)
            start = self._seconds_to_srt_time(current_time)
            end = self._seconds_to_srt_time(current_time + duration)
            text = scene.get("narration_text", "")
            lines.append(f"{idx}")
            lines.append(f"{start} --> {end}")
            lines.append(text)
            lines.append("")
            current_time += duration
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_path

    @staticmethod
    def _seconds_to_srt_time(total_seconds: float) -> str:
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        millis = int((total_seconds - int(total_seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"
