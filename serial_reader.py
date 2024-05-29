from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
import serial
import asyncio
from collections import deque
import time
import random


@dataclass()
class SensorReadouts:
    humidity_one: float
    temperature_one: float

    humidity_two: float
    temperature_two: float

    humidity_three: float
    temperature_three: float

    has_vibration: bool
    is_relay_activated: bool


class AbstractSerialProvider(ABC):
    @abstractmethod
    def get_current_readouts(self) -> SensorReadouts:
        pass


class MockSerialProvider(AbstractSerialProvider):
    def __init__(self) -> None:
        super().__init__()
        random.seed(time.time())

    @staticmethod
    def _generate_variation() -> float:
        variation = random.uniform(-10, 10)
        return round(variation, 2)

    def get_current_readouts(self) -> SensorReadouts:
        return SensorReadouts(
            humidity_one=50.0 + MockSerialProvider._generate_variation(),
            temperature_one=25.0 + MockSerialProvider._generate_variation(),
            humidity_two=52.0 + MockSerialProvider._generate_variation(),
            temperature_two=25.0 + MockSerialProvider._generate_variation(),
            humidity_three=53.0 + MockSerialProvider._generate_variation(),
            temperature_three=27.0 + MockSerialProvider._generate_variation(),
            has_vibration=random.random() > 0.5,
            is_relay_activated=random.random() > 0.5,
        )


class SerialProvider(AbstractSerialProvider):
    _current_readouts: SensorReadouts
    _is_reading: bool = False

    def __init__(self) -> None:
        self._serial = serial.Serial("/dev/ttyACM0", 9800, timeout=1)
        self._read_sensors_task = asyncio.create_task(self._read_sensors())

    def stop_reading(self):
        self._is_reading = False

    async def _read_sensors(self) -> None:
        loop = asyncio.get_event_loop()
        self._is_reading = True
        while self._is_reading:
            # string is in format of "{humidity} {temperature}"
            packed_string = await loop.run_in_executor(None, self._serial.readline)
            values = packed_string.split()
            self._current_readouts = SensorReadouts(
                humidity_one=float(values[0]),
                temperature_one=float(values[1]),
                humidity_two=float(values[2]),
                temperature_two=float(values[3]),
                humidity_three=float(values[4]),
                temperature_three=float(values[5]),
                has_vibration=bool(values[6]),
                is_relay_activated=bool(values[7]),
            )

    def get_current_readouts(self) -> SensorReadouts:
        return self._current_readouts


async def set_interval(func: Callable, interval: int):
    while True:
        await asyncio.sleep(interval)
        func()


class SerialReader:
    _historic_vibration_data: deque[int]
    _historic_relay_data: deque[int]
    _current_readouts: SensorReadouts

    def __init__(
        self, provider: AbstractSerialProvider, historic_data_len: int = 120
    ) -> None:
        self._provider = provider
        self._current_readouts = provider.get_current_readouts()
        self._historic_vibration_data = deque(maxlen=historic_data_len)
        self._historic_relay_data = deque(maxlen=historic_data_len)
        # TODO: check if coroutine is cleaned properly
        asyncio.ensure_future(self._run_query_provider())

    async def _run_query_provider(self):
        while True:
            self._query_provider()
            await asyncio.sleep(1)  # Wait for 1 second before next call

    @property
    def current_readouts(self) -> SensorReadouts:
        return self._current_readouts

    @property
    def historic_vibration_data(self) -> list[int]:
        return list(self._historic_vibration_data)

    @property
    def historic_relay_data(self) -> list[int]:
        return list(self._historic_relay_data)

    def _query_provider(self):
        readouts = self._provider.get_current_readouts()
        self._current_readouts = readouts
        self._historic_vibration_data.append(int(readouts.has_vibration))
        self._historic_relay_data.append(int(readouts.is_relay_activated))
