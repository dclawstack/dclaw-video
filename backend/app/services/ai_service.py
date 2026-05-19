import json
import re
from typing import Any

import httpx

from app.core.config import settings


class AIService:
    def __init__(self) -> None:
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model or "meta-llama/llama-3.1-8b-instruct"
        self.base_url = "https://openrouter.ai/api/v1"

    async def chat(
        self, messages: list[dict[str, str]], temperature: float = 0.7
    ) -> str:
        if not self.api_key:
            return (
                "OpenRouter API key not configured. "
                "Set DCLAW_OPENROUTER_API_KEY."
            )

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://dclaw.video",
                    "X-Title": "DClaw Video",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                },
            )
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
            return str(data["choices"][0]["message"]["content"])

    async def parse_script_to_scenes(
        self, script: str, tone: str = "professional", max_scenes: int = 10
    ) -> list[dict[str, Any]]:
        system_prompt = (
            f"You are a video director. Break the script into {max_scenes} or fewer scenes. "
            f"Each scene needs: narration_text, visual_prompt, duration_seconds (3–15s). "
            f"Tone: {tone}. Return ONLY valid JSON array. No markdown."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": script},
        ]
        content = await self.chat(messages, temperature=0.3)
        try:
            parsed: list[dict[str, Any]] = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            match = re.search(r"\[.*\]", content, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                return parsed
            raise ValueError(
                f"Failed to parse AI response as JSON: {content[:200]}"
            )

    async def improve_script(self, script: str, feedback: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You write SaaS product video scripts.",
            },
            {
                "role": "user",
                "content": f"Script:\n{script}\n\nFeedback: {feedback}",
            },
        ]
        return await self.chat(messages, temperature=0.7)


ai_service = AIService()
