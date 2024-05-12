import abc
from typing import Set

from sqlalchemy import select

from sensorprocessor.domain import model


class AbstractSensorRepository(abc.ABC):

    def __init__(self):
        self.seen: Set[model.Sensordata] = set()

    def get(self, sensor: str) -> model.Sensordata:
        sensordata = self._get(sensor)
        if sensordata:
            self.seen.add(sensordata)
        return sensordata

    def add(self, sensordata: model.Sensordata):
        self._add(sensordata)
        self.seen.add(sensordata)

    @abc.abstractmethod
    def _get(self, sensor: str) -> model.Sensordata:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, sensordata: model.Sensordata):
        raise NotImplementedError


class SqlAlchemySensorRepository(AbstractSensorRepository):

    def __init__(self, session):
        self.session = session
        super().__init__()

    def _get(self, sensor: str):
        sensordata = (
            self.session.execute(
                select(model.Sensordata).where(model.Sensordata.sensor == sensor)
            )
            .scalars()
            .first()
        )
        return sensordata

    def _add(self, sensordata):
        self.session.add(sensordata)
