import io

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

from app.core.config import settings


class TTSService:
    def __init__(self, model_path: str | None = None, voices_path: str | None = None):
        self.model_path = model_path or settings.kokoro_model_path
        self.voices_path = voices_path or settings.kokoro_voices_path
        self.kokoro: Kokoro | None = None

    def _load(self) -> Kokoro:
        if self.kokoro is None:
            self.kokoro = Kokoro(self.model_path, self.voices_path)
        return self.kokoro

    def synthesize(self, text: str, voice_id: str = "af_bella", speed: float = 1.0) -> bytes:
        kokoro = self._load()
        samples, sample_rate = kokoro.create(
            text,
            voice=voice_id,
            speed=speed,
            lang="en-us",
        )
        buffer = io.BytesIO()
        sf.write(buffer, np.array(samples), sample_rate, format="WAV")
        return buffer.getvalue()
