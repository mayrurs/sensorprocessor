import abc

from dataclasses import dataclass
from datetime import datetime

class Event(abc.ABC):
    pass

@dataclass
class RawDataCreated(Event):
    sensor: str
    value: int
    timestamp: datetime
