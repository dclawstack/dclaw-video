import json
import httpx
from app.core.config import settings


class ComfyUIClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.comfyui_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=300.0)

    async def queue_prompt(self, workflow: dict) -> str:
        payload = {"prompt": workflow}
        resp = await self.client.post("/prompt", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("prompt_id", "")

    async def get_history(self, prompt_id: str) -> dict:
        resp = await self.client.get(f"/history/{prompt_id}")
        resp.raise_for_status()
        return resp.json()

    async def upload_image(self, image_path: str, name: str = "input.png") -> dict:
        with open(image_path, "rb") as f:
            files = {"image": (name, f, "image/png")}
            resp = await self.client.post("/upload/image", files=files)
        resp.raise_for_status()
        return resp.json()

    def build_flux_workflow(self, prompt: str, width: int = 1280, height: int = 720) -> dict:
        # Minimal ComfyUI workflow JSON for FLUX image generation
        # Users should replace node IDs with their actual workflow
        return {
            "1": {
                "inputs": {"width": width, "height": height, "batch_size": 1},
                "class_type": "EmptyLatentImage",
            },
            "2": {
                "inputs": {"text": prompt, "clip": ["3", 0]},
                "class_type": "CLIPTextEncode",
            },
            "3": {
                "inputs": {"ckpt_name": "flux1-dev.safetensors"},
                "class_type": "CheckpointLoaderSimple",
            },
            "4": {
                "inputs": {
                    "seed": 42,
                    "steps": 20,
                    "cfg": 1.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "model": ["3", 0],
                    "positive": ["2", 0],
                    "negative": ["2", 0],
                    "latent_image": ["1", 0],
                },
                "class_type": "KSampler",
            },
            "5": {
                "inputs": {"samples": ["4", 0], "vae": ["3", 2]},
                "class_type": "VAEDecode",
            },
            "6": {
                "inputs": {"filename_prefix": "dclaw", "images": ["5", 0]},
                "class_type": "SaveImage",
            },
        }

    def build_animatediff_workflow(self, prompt: str, width: int = 512, height: int = 512, frames: int = 16) -> dict:
        return {
            "1": {
                "inputs": {"width": width, "height": height, "batch_size": frames},
                "class_type": "EmptyLatentImage",
            },
            "2": {
                "inputs": {"text": prompt, "clip": ["3", 0]},
                "class_type": "CLIPTextEncode",
            },
            "3": {
                "inputs": {"ckpt_name": "animatediff_model.safetensors"},
                "class_type": "CheckpointLoaderSimple",
            },
            "4": {
                "inputs": {
                    "seed": 42,
                    "steps": 20,
                    "cfg": 7.0,
                    "sampler_name": "euler_ancestral",
                    "scheduler": "normal",
                    "model": ["3", 0],
                    "positive": ["2", 0],
                    "negative": ["2", 0],
                    "latent_image": ["1", 0],
                },
                "class_type": "KSampler",
            },
            "5": {
                "inputs": {"samples": ["4", 0], "vae": ["3", 2]},
                "class_type": "VAEDecode",
            },
            "6": {
                "inputs": {"filename_prefix": "dclaw_clip", "images": ["5", 0]},
                "class_type": "SaveImage",
            },
        }
