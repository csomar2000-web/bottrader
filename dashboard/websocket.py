import asyncio
from fastapi import WebSocket
from typing import Dict, List
from core.logger import trading_logger

class WebSocketManager:
    def __init__(self):
        self.active: List[WebSocket] = []
        self.queue = asyncio.Queue()
        self.running = False

    async def start(self):
        self.running = True
        asyncio.create_task(self._broadcast_loop())

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    async def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def push(self, data: Dict):
        await self.queue.put(data)

    async def _broadcast_loop(self):
        while self.running:
            msg = await self.queue.get()
            for ws in list(self.active):
                try:
                    await ws.send_json(msg)
                except:
                    await self.disconnect(ws)

ws_manager = WebSocketManager()
