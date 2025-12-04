from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from dashboard.heatmap.heatmap_renderer import HeatmapRenderer

class HeatmapServer:
    def __init__(self, data):
        self.data = data
        self.app = FastAPI()

        @self.app.get("/heatmap/html")
        def html():
            return HTMLResponse(HeatmapRenderer(self.data).html())

        @self.app.get("/heatmap/json")
        def json():
            return JSONResponse(self.data.snapshot())

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=9998)
