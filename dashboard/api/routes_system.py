from fastapi import APIRouter
import time

system_router = APIRouter()

@system_router.get("/status")
async def system_status():
    return {"status": "ok", "timestamp": time.time()}

@system_router.get("/heartbeat")
async def heartbeat():
    return {"alive": True}
