import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/playback")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send current playback state immediately after connection
            current_state = websocket.app.state.spotify_client.playback_state.get_state()
            await websocket.send_json({
                "type": "playback_update",
                "data": current_state
            })
            # Wait for client ping to keep connection alive
            await websocket.receive_text()
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")