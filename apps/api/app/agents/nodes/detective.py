"""Detective node"""

from __future__ import annotations

import time

from app.agents.events import (
    RUNS,
    DecideEvent,
    MCPCallEvent,
    MCPResultEvent,
    ReasonEvent,
)
from app.agents.state import MinariState
from app.core.logging import get_logger
from app.services import gitlab_mcp
from app.services.embeddings import embed_text
from app.services.fixes.languages import detect_language
from app.services.llm.deepseek import diagnose_with_deepseek
from app.services.llm.gemini import diagnose_with_gemini
from app.services.llm.prompts import build_diagnosis_prompt
from app.services.llm.router import choose_model
from app.services.similarity import find_similar_diagnoses

log = get_logger(__name__)






async def detective_node(state: MinariState) -> MinariState:
    bus = RUNS.get(state.run_id)

    async def emit(event) -> None:
        if bus is not None:
            await bus.emit(event)

    started = time.perf_counter()



    # Evidence
    await emit(MCPCallEvent(stage="detective", tool="get_file_contents",
                            params_summary=f"{state.project_id}:{state.file_path}"))
    src, lat = await gitlab_mcp.get_raw_file(state.project_id, state.file_path, state.ref)
    state.test_source = src
    await emit(MCPResultEvent(stage="detective", tool="get_file_contents",
                              bytes=len(src), latency_ms=lat))

    if state.pipeline_id:
        await emit(MCPCallEvent(stage="detective", tool="get_pipeline_jobs",
                                params_summary=f"pipeline {state.pipeline_id}"))
        logtext, lat = await gitlab_mcp.get_pipeline_jobs(state.project_id, state.pipeline_id)
        state.pipeline_log = logtext
        await emit(MCPResultEvent(stage="detective", tool="get_pipeline_jobs",
                                  bytes=len(logtext), latency_ms=lat))

    await emit(MCPCallEvent(stage="detective", tool="git_blame", params_summary=state.file_path))
    blame, lat = await gitlab_mcp.get_git_blame(state.project_id, state.file_path, state.ref)
    state.git_blame = blame
    await emit(MCPResultEvent(stage="detective", tool="git_blame",
                              bytes=len(blame), latency_ms=lat))





    # Language/framework detection (stored on the test row)
    info = detect_language(state.file_path)
    if info is not None:
        state.language, state.framework = info.language, info.framework

    # Embed + retrieve. Store the embedding as a real field so it survives the
    # graph's model_validate round-trip and reaches upsert_test for pgvector.
    try:
        embedding = await embed_text(src)
        state.embedding = embedding
        state.similar_examples = await find_similar_diagnoses(state.project_id, embedding)
        if state.similar_examples:
            await emit(ReasonEvent(
                stage="detective",
                text=f"Retrieved {len(state.similar_examples)} similar past "
                     "diagnoses for grounding."))
    except Exception as exc:
        log.warning("detective.embed.skip", error=str(exc))





    # Route
    route = choose_model(state.pfs_score)
    state.model_used = route.model
    await emit(DecideEvent(stage="detective", text=route.reason))




    # Diagnose
    prompt = build_diagnosis_prompt(
        test_name=state.test_name, test_source=src, pipeline_log=state.pipeline_log,
        git_blame=blame, pfs_score=state.pfs_score, similar_examples=state.similar_examples,
    )
    if route.provider == "deepseek":
        diagnosis, _, trace = await diagnose_with_deepseek(route.model, prompt)
        if trace:
            await emit(ReasonEvent(stage="detective", text=trace[:1500]))
    else:
        diagnosis, _ = await diagnose_with_gemini(route.model, prompt)

    for step in diagnosis.reasoning_chain:
        await emit(ReasonEvent(stage="detective", text=f"{step.step}. {step.observation}"))

    state.diagnosis = diagnosis
    state.status = "done" if diagnosis.is_confident else "degraded"
    log.info("detective.done", run_id=state.run_id, category=diagnosis.category.value,
             confidence=diagnosis.confidence, ms=int((time.perf_counter() - started) * 1000))
    return state
