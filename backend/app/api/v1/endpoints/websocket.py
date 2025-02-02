from fastapi import APIRouter, WebSocket
from app.services.websocket_manager import websocket_manager

router = APIRouter()

@router.websocket("/playback")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        websocket_manager.disconnect(websocket)
