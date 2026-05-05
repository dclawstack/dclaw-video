from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from celery.result import AsyncResult
from app.core.celery_app import celery_app

router = APIRouter(tags=["websocket"])


@router.websocket("/api/v1/render/{job_id}/progress")
async def render_progress_ws(websocket: WebSocket, job_id: str):
    await websocket.accept()
    try:
        while True:
            result = AsyncResult(job_id, app=celery_app)
            data = {
                "job_id": job_id,
                "status": result.status,
                "progress": result.info.get("progress", 0) if result.info else 0,
                "logs": result.info.get("logs", "") if result.info else "",
            }
            await websocket.send_json(data)
            if result.ready():
                break
            await websocket.receive_text()  # keepalive or client ping
    except WebSocketDisconnect:
        pass
