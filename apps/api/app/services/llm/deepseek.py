"""Deepseek-r1 diagnosis"""





from __future__ import annotations
import json
import time
import httpx
from pydantic import ValidationError
from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.diagnosis import Diagnosis
from app.services.llm.prompts import SYSTEM_PROMPT, build_repair_prompt






log = get_logger(__name__)
MAX_REPAIRS = 2







async def diagnose_with_deepseek(model: str, prompt: str) -> tuple[Diagnosis, int, str]:
    """Return (Diagnosis, latency_ms, reasoning_trace)."""
    s = get_settings()
    if s.deepseek_api_key is None:
        raise RuntimeError("MINARI_DEEPSEEK_API_KEY is not set")

    schema_hint = (
        "Respond with ONLY a JSON object matching this schema (no prose, no fences): "
        f"{Diagnosis.model_json_schema()}"
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{prompt}\n\n{schema_hint}"},
    ]
    started = time.perf_counter()
    reasoning_trace = ""
    async with httpx.AsyncClient(base_url=s.deepseek_base_url, timeout=60) as client:
        for attempt in range(MAX_REPAIRS + 1):
            resp = await client.post(
                "/chat/completions",
                headers={"Authorization": f"Bearer {s.deepseek_api_key.get_secret_value()}"},
                json={"model": model, "messages": messages, "temperature": 0.2},
            )
            resp.raise_for_status()
            choice = resp.json()["choices"][0]["message"]
            reasoning_trace = choice.get("reasoning_content", "") or reasoning_trace
            raw = choice["content"].strip().removeprefix("```json").removeprefix("```").removesuffix("```")
            try:
                diagnosis = Diagnosis.model_validate_json(raw)
                latency = int((time.perf_counter() - started) * 1000)
                log.info("deepseek.diagnosis.ok", attempt=attempt, latency_ms=latency)
                return diagnosis, latency, reasoning_trace
            except (ValidationError, json.JSONDecodeError) as err:
                log.warning("deepseek.diagnosis.repair", attempt=attempt, error=str(err)[:300])
                messages.append({"role": "assistant", "content": raw})
                messages.append({"role": "user", "content": build_repair_prompt(raw, str(err))})
    raise RuntimeError("DeepSeek-R1 output failed schema after repairs")