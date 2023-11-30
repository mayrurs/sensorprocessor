from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass

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

    def __repr__(self) -> str:
        return f"Sensordata({self.sensor!r})"

