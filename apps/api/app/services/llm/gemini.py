"""Gemini diagnosis via official genai sdk"""


from __future__ import annotations
import time
from google import genai
from google.genai import types
from pydantic import ValidationError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.diagnosis import Diagnosis
from app.services.llm.prompts import SYSTEM_PROMPT, build_repair_prompt










log = get_logger(__name__)
_client: genai.Client | None = None
MAX_REPAIRS = 2



def _client_singleton() -> genai.Client:
    global _client
    if _client is None:
        key = get_settings().gemini_api_key
        if key is None:
            raise RuntimeError("MINARI_GEMINI_API_KEY is not set")
        _client = genai.Client(api_key=key.get_secret_value())
    return _client









class _Retryable(Exception):
    ...





@retry(
    retry=retry_if_exception_type(_Retryable),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    stop=stop_after_attempt(3),
    reraise=True,
)

async def _generate(model: str, contents: list[str]) -> str:
    try:
        resp = await _client_singleton().aio.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=Diagnosis,
                temperature=0.2,
                # 2.5 Pro spends output tokens on internal "thinking" before the
                # JSON; 2048 gets eaten by thinking and truncates the JSON. 8192
                # leaves ample room. (google-genai 1.2.0 has no thinking_budget.)
                max_output_tokens=8192,
            ),
        )
        # When the model hits MAX_TOKENS mid-thought, resp.text is None — surface
        # it so the repair loop (or a clearer error) handles it rather than passing
        # None into model_validate_json.
        if resp.text is None:
            raise _Retryable("empty response (no text part — likely truncated)")
        return resp.text
    except Exception as exc:  
        msg = str(exc).lower()
        if any(k in msg for k in ("429", "503", "deadline", "timeout", "unavailable")):
            raise _Retryable(str(exc)) from exc
        raise





async def diagnose_with_gemini(model: str, prompt: str) -> tuple[Diagnosis, int]:
    """Return (Diagnosis, latency_ms). Runs the repair loop on validation failure."""
    started = time.perf_counter()
    contents = [prompt]
    last_raw = ""
    for attempt in range(MAX_REPAIRS + 1):
        last_raw = await _generate(model, contents)
        try:
            diagnosis = Diagnosis.model_validate_json(last_raw)
            latency = int((time.perf_counter() - started) * 1000)
            log.info("gemini.diagnosis.ok", model=model, attempt=attempt, latency_ms=latency)
            return diagnosis, latency
        except ValidationError as ve:
            log.warning("gemini.diagnosis.repair", model=model, attempt=attempt, error=str(ve)[:300])
            contents = [prompt, build_repair_prompt(last_raw, str(ve))]
    raise RuntimeError("Gemini structured output failed schema after repairs")