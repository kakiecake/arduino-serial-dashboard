from dataclasses import dataclass
from dotenv import dotenv_values
from pathlib import Path
from typing import Optional
import functools


@dataclass()
class AppConfig:
    serial_port: Optional[str]
    serial_port_baudrate: int


@functools.cache
def config() -> AppConfig:
    dotenv_path = Path.cwd() / ".env"
    loaded_config: dict[str, str | None]
    if dotenv_path.exists():
        loaded_config = dotenv_values(dotenv_path)
    else:
        loaded_config = {}

    serial_port = loaded_config.get("SERIAL_PORT", "/dev/ttyACM0")
    baudrate = loaded_config.get("SERIAL_PORT_BAUDRATE")
    baudrate = (int(baudrate) or None) if baudrate else None

    return AppConfig(
        serial_port=serial_port,
        serial_port_baudrate=baudrate or 9600,
    )
