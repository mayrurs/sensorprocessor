from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass

from . import events

from typing import List

@dataclass
class Rawdata:
    sensor: str
    value: int 
    timestamp: datetime

class Sensordata:
    def __init__(self, sensor: str, rawdata: List[Rawdata] = []):
        self.sensor = sensor
        self.rawdata: List[Rawdata] = rawdata
        self.events = []

    def add_raw_data(self, rawdata: Rawdata):
        self.rawdata.append(rawdata)
        self.events.append(
                events.RawDataCreated(rawdata.sensor, 
                                      rawdata.value,
                                      rawdata.timestamp)
                )

    def __repr__(self) -> str:
        return f"Sensordata({self.sensor!r})"

