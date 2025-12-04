import uvicorn
from fastapi import FastAPI
from dashboard.api.routes_trades import trades_router
from dashboard.api.routes_metrics import metrics_router
from dashboard.api.routes_system import system_router
from dashboard.websocket import ws_manager

app = FastAPI()
app.include_router(trades_router, prefix="/trades")
app.include_router(metrics_router, prefix="/metrics")
app.include_router(system_router, prefix="/system")

@app.on_event("startup")
async def start_ws():
    await ws_manager.start()

def run():
    uvicorn.run(app, host="0.0.0.0", port=8080)
