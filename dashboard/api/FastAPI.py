from fastapi import APIRouter, WebSocket
from dashboard.websocket import ws_manager

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)
    while True:
        try:
            await ws.receive_text()
        except:
            await ws_manager.disconnect(ws)
            break
