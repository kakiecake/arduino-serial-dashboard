from dataclasses import asdict
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import serial

from .serial_reader import (
    AbstractSerialProvider,
    MockSerialProvider,
    SerialProvider,
    SerialReader,
)
from .config import config

config = config()

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

serial_provider: AbstractSerialProvider

logger.info(config)

if config.serial_port:
    serial = serial.Serial(config.serial_port, config.serial_port_baudrate, timeout=1)
    logger.info("Using real serial port")
    serial_provider = SerialProvider(serial, logger)
else:
    logger.info("Using mock serial port")
    serial_provider = MockSerialProvider()

serial_reader = SerialReader(serial_provider, query_interval_seconds=2)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    data = asdict(serial_reader.current_readouts)
    data["historic_vibration_data"] = serial_reader.historic_vibration_data
    data["historic_relay_data"] = serial_reader.historic_relay_data
    return templates.TemplateResponse(
        request=request,
        name="index.html",
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
