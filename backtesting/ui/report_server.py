from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from backtesting.ui.report_renderer import ReportRenderer

class ReportServer:
    def __init__(self, data):
        self.data = data
        self.app = FastAPI()

        @self.app.get("/report/html")
        def html():
            return HTMLResponse(ReportRenderer(self.data).html())

        @self.app.get("/report/json")
        def json():
            return JSONResponse(self.data.snapshot())

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=9999)
