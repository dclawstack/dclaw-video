from fastapi import APIRouter

router = APIRouter()


@router.get("/ws/subscribe/{task_id}")
async def websocket_placeholder() -> dict[str, str]:
    return {"message": "WebSocket endpoint - implement with FastAPI websockets"}
