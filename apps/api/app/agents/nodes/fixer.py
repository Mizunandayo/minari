"""Fixer node"""

from __future__ import annotations

import time

from app.agents.events import RUNS, DecideEvent, FixEvent, ReasonEvent
from app.agents.state import MinariState
from app.core.config import get_settings
from app.core.logging import get_logger
from app.schemas.fix import FixCandidate, FixCandidates
from app.services.fixes.assertions import assertions_preserved
from app.services.fixes.diffing import imports_present, unified_diff
from app.services.fixes.languages import detect_language
from app.services.fixes.syntax import is_syntax_valid
from app.services.llm.fixer import generate_fixes

log = get_logger(__name__)





async def fixer_node(state: MinariState) -> MinariState:
    bus = RUNS.get(state.run_id)

    async def emit(event) -> None:
        if bus is not None:
            await bus.emit(event)


    if state.diagnosis is None or not state.diagnosis.is_confident:
        return state
    if not state.test_source:
        await emit(DecideEvent(stage="fixer",
                               text="No test source available — skipping fix generation."))
        return state
    

    info = detect_language(state.file_path)
    if info is None:
        await emit(DecideEvent(stage="fixer",
                               text=f"Unsupported language for {state.file_path} — skipping."))
        return state
    

    started = time.perf_counter()
    # Fix generation is mechanical relative to diagnosis — Flash is ~5-6x faster
    # than Pro and avoids the long "thinking" pause, keeping the demo snappy.
    fix_model = get_settings().gemini_flash_model
    await emit(DecideEvent(
        stage="fixer",
        text=f"Generating 3 fix candidates for a '{state.diagnosis.category.value}' root cause "
             f"({info.language}/{info.framework}) with {fix_model}.",
    ))


    async def _generate_and_filter() -> list[FixCandidate]:
        raw, _ = await generate_fixes(
            fix_model,
            test_name=state.test_name, language=info.language, framework=info.framework,
            test_source=state.test_source, diagnosis=state.diagnosis,
        )
        survivors: list[FixCandidate] = []
        for draft in sorted(raw.candidates, key=lambda x: x.rank):
            # Enrich the model's draft with our computed, validated fields.
            c = FixCandidate(**draft.model_dump())
            c.syntax_valid = is_syntax_valid(info.grammar, c.fixed_source)
            c.assertions_safe = assertions_preserved(
                info.grammar, state.test_source, c.fixed_source)
            c.fix_diff = unified_diff(state.test_source, c.fixed_source, state.file_path)

            if not c.syntax_valid:
                await emit(DecideEvent(
                    stage="fixer",
                    text=f"Candidate {c.rank} rejected — generated code is "
                         "not syntactically valid."))
                continue
            if not c.assertions_safe:
                await emit(DecideEvent(
                    stage="fixer",
                    text=f"Candidate {c.rank} rejected — it modifies a test "
                         "assertion (safety boundary)."))
                continue
            if not imports_present(info.grammar, c.fixed_source):
                await emit(ReasonEvent(
                    stage="fixer",
                    text=f"Candidate {c.rank}: heads-up — a referenced module "
                         "may be missing an import."))

            survivors.append(c)
            await emit(FixEvent(
                stage="fixer", rank=c.rank, fix_category=c.fix_category.value,
                confidence=c.confidence, explanation=c.explanation, fix_diff=c.fix_diff,
                language=info.language, syntax_valid=True, assertions_safe=True,
            ))
        return survivors


    safe = await _generate_and_filter()
    # Flash at temperature occasionally emits a whole batch of invalid candidates.
    # One regeneration recovers most of those without dead-ending the pipeline.
    if not safe:
        await emit(DecideEvent(
            stage="fixer",
            text="No candidate passed the safety gates — regenerating once."))
        safe = await _generate_and_filter()


    safe.sort(key=lambda x: x.confidence, reverse=True)
    for i, c in enumerate(safe, start=1):
        c.rank = i
    state.fixes = FixCandidates(candidates=safe) if safe else None


    if not safe:
        await emit(DecideEvent(
            stage="fixer",
            text="No candidate passed the safety gates — handing off "
                 "for manual review."))
        state.status = "degraded"


    log.info("fixer.done", run_id=state.run_id,
             safe=len(safe), ms=int((time.perf_counter() - started) * 1000))
    return state
