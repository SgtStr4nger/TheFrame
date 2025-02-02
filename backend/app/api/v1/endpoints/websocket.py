from fastapi import APIRouter, WebSocket,WebSocketDisconnect


router = APIRouter()


@router.websocket("/playback")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client disconnected")
        while True:
            # Add a receive call to detect disconnections
            await websocket.receive_text()
            current_state = spotify_client.playback_state.get_state()
            await websocket.send_json({
                "type": "playback_update",
                "data": current_state
            })
    except WebSocketDisconnect:
        print("Client disconnected")
