import abc
from dataclasses import dataclass
from datetime import datetime


class Command(abc.ABC):
    pass


@dataclass
class CreateRawData(Command):
    sensor: str
    value: int
    timestamp: datetime
