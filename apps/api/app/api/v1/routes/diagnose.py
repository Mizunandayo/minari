"""Diagnosis API"""

import asyncio
import json
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sse_starlette.sse import EventSourceResponse
from app.agents.events import RUNS, DoneEvent, ErrorEvent, EventBus
from app.agents.graph import GRAPH
from app.agents.state import MinariState
from app.core.logging import get_logger
from app.core.rate_limit import DIAGNOSIS_LIMIT, limiter
from app.core.security import mint_stream_token, require_api_key, verify_stream_token
from app.repositories.diagnoses_repo import create_run, finalize_run
from app.repositories.tests_repo import upsert_test
from app.schemas.api import DiagnoseAccepted, DiagnoseRequest, DiagnosisResult
from app.services.pfs.engine import calculate_pfs 








log = get_logger(__name__)
router = APIRouter()








async def _run_pipeline(state: MinariState, bus: EventBus) -> None:
    try:
        result: MinariState = await GRAPH.ainvoke(state)
        final = MinariState.model_validate(result)
        test_id = await upsert_test(
            project_id=final.project_id, file_path=final.file_path,
            test_name=final.test_name, language=final.language,
            framework=final.framework, embedding=final.embedding,
        )
        await finalize_run(
            run_id=final.run_id, test_id=test_id, status=final.status,
            pfs_score=final.pfs_score, model_used=final.model_used or "",
            diagnosis=final.diagnosis, latency_ms=0, error=None,
        )
        if final.diagnosis:
            await bus.emit(DoneEvent(stage="system",
                                     confidence=final.diagnosis.confidence,
                                     category=final.diagnosis.category.value))
    except Exception as exc: 
        log.error("diagnose.failed", run_id=state.run_id, error=str(exc))
        await finalize_run(run_id=state.run_id, test_id=None, status="failed",
                           pfs_score=state.pfs_score, model_used="", diagnosis=None,
                           latency_ms=0, error=str(exc)[:500])
        await bus.emit(ErrorEvent(stage="system", message="Diagnosis failed. See server logs."))
    finally:
        await bus.close()













@router.post("/diagnose", response_model=DiagnoseAccepted, status_code=status.HTTP_202_ACCEPTED,
             dependencies=[Depends(require_api_key)])
@limiter.limit(DIAGNOSIS_LIMIT)
async def trigger_diagnosis(request: Request, body: DiagnoseRequest) -> DiagnoseAccepted:
    run_id = str(uuid.uuid4())
    bus = EventBus()
    RUNS[run_id] = bus
    state = MinariState(
        run_id=run_id, project_id=body.project_id, file_path=body.file_path,
        test_name=body.test_name, ref=body.ref, pipeline_id=body.pipeline_id,
        pfs_score=50.0,  
    )
    await create_run(run_id=run_id, project_id=body.project_id,
                     file_path=body.file_path, test_name=body.test_name)
    asyncio.create_task(_run_pipeline(state, bus))  
    return DiagnoseAccepted(
        run_id=run_id,
        stream_path=f"/api/v1/diagnose/{run_id}/stream",
        stream_token=mint_stream_token(run_id),
    )














@router.get("/diagnose/{run_id}/stream")
async def stream_diagnosis(run_id: str, token: str, request: Request) -> EventSourceResponse:
    if not verify_stream_token(run_id, token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid stream token")
    bus = RUNS.get(run_id)
    if bus is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown or completed run")

    async def gen():
        try:
            async for event in bus.stream():
                if await request.is_disconnected():
                    break
                yield {"event": event.type, "data": json.dumps(event.model_dump())}
        finally:
            RUNS.pop(run_id, None)

    return EventSourceResponse(gen(), ping=15) 