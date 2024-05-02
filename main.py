import asyncio
from dataclasses import asdict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

from serial_reader import AbstractSerialProvider, MockSerialProvider, SerialReader

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

serial_reader = SerialReader(MockSerialProvider())


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    data = asdict(serial_reader.current_readouts)
    data["historic_vibration_data"] = serial_reader.historic_vibration_data
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        # headers={"HX-Trigger": json.dumps(htmx_event)},
        context=data,
    )


@app.get("/readouts", response_class=HTMLResponse)
async def get_readouts(request: Request):
    data = asdict(serial_reader.current_readouts)
    htmx_event = {"dataUpdated": data}
    return templates.TemplateResponse(
        request=request,
        name="readouts.html",
        headers={"HX-Trigger": json.dumps(htmx_event)},
        context=data,
    )
