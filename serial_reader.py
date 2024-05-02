from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Deque
import serial
import asyncio
from collections import deque


@dataclass()
class SensorReadouts:
    humidity: float
    temperature: float
    has_vibration: bool
    is_relay_activated: bool


class AbstractSerialProvider(ABC):
    @abstractmethod
    def get_current_readouts(self) -> SensorReadouts:
        pass


class MockSerialProvider(AbstractSerialProvider):
    _readouts = SensorReadouts(
        humidity=50.0, temperature=25.0, has_vibration=True, is_relay_activated=True
    )

    def get_current_readouts(self) -> SensorReadouts:
        return self._readouts


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
            packed_string = await loop.run_in_executor(None, self._serial.readline)
            values = packed_string.split()
            self._current_readouts = SensorReadouts(
                humidity=float(values[0]),
                temperature=float(values[1]),
                has_vibration=bool(values[2]),
                is_relay_activated=bool(values[3]),
            )

    def get_current_readouts(self) -> SensorReadouts:
        return self._current_readouts


async def set_interval(func: Callable, interval: int):
    while True:
        await asyncio.sleep(interval)
        func()


class SerialReader:
    _historic_vibration_data: deque[int]
    _current_readouts: SensorReadouts

    def __init__(
        self, provider: AbstractSerialProvider, historic_data_len: int = 120
    ) -> None:
        self._provider = provider
        self._current_readouts = provider.get_current_readouts()
        self._historic_vibration_data = deque(maxlen=historic_data_len)
        # TODO: clean the coroutine
        asyncio.create_task(set_interval(self._query_provider, 1000))

    @property
    def current_readouts(self) -> SensorReadouts:
        return self._current_readouts

    @property
    def historic_vibration_data(self) -> list[int]:
        return list(self._historic_vibration_data)

    def _query_provider(self):
        print("_query_provider")
        readouts = self._provider.get_current_readouts()
        self._current_readouts = readouts
        self._historic_vibration_data.append(int(readouts.has_vibration))
        print(self._historic_vibration_data)
