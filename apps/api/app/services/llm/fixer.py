"""Fix generation via gemini structured output"""

from __future__ import annotations

import time

from google.genai import types
from pydantic import ValidationError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.logging import get_logger
from app.schemas.diagnosis import Diagnosis
from app.schemas.fix import FixDrafts
from app.services.llm.fix_prompts import (
    FIX_SYSTEM_PROMPT,
    build_fix_prompt,
    build_fix_repair_prompt,
)
from app.services.llm.gemini import _client_singleton, _Retryable

log = get_logger(__name__)
MAX_REPAIRS = 2





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
                system_instruction=FIX_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=FixDrafts,
                temperature=0.3,
                # Three FULL rewritten files + Gemini 2.5 Pro "thinking" tokens far
                # exceed the 8192 a single diagnosis needs. Too low -> resp.text is
                # None (truncated) -> retry storm -> the pipeline appears to hang.
                max_output_tokens=24576,
            ),
        )
        if resp.text is None:
            raise _Retryable("empty response (truncated before JSON)")
        return resp.text
    except Exception as exc:
        msg = str(exc).lower()
        if any(k in msg for k in ("429", "503", "deadline", "timeout", "unavailable")):
            raise _Retryable(str(exc)) from exc
        raise











async def generate_fixes(
    model: str, *, test_name: str, language: str, framework: str,
    test_source: str, diagnosis: Diagnosis,
) -> tuple[FixDrafts, int]:
    """Return (FixDrafts, latency_ms)"""
    started = time.perf_counter()
    prompt = build_fix_prompt(
        test_name=test_name, language=language, framework=framework,
        test_source=test_source, diagnosis=diagnosis,
    )
    contents = [prompt]
    last_raw = ""
    for attempt in range(MAX_REPAIRS + 1):
        last_raw = await _generate(model, contents)
        try:
            fixes = FixDrafts.model_validate_json(last_raw)
            latency = int((time.perf_counter() - started) * 1000)
            log.info("fixer.ok", model=model, attempt=attempt,
                     n=len(fixes.candidates), latency_ms=latency)
            return fixes, latency
        except ValidationError as ve:
            log.warning("fixer.repair", model=model, attempt=attempt, error=str(ve)[:300])
            contents = [prompt, build_fix_repair_prompt(last_raw, str(ve))]
    raise RuntimeError("Fixer structured output failed schema after repairs")