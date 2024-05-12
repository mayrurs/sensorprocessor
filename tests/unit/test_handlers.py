import pytest

from datetime import datetime
from re import A

from typing import List

from sensorprocessor.adapters import repository
from sensorprocessor.domain import commands, model
from sensorprocessor.service_layers import messagebus, unit_of_work


class FakeRepository(repository.AbstractSensorRepository):

    def __init__(self, sensordata: List = []):
        super().__init__()
        self._sensordata = sensordata

    def _add(self, sensordata: model.Sensordata):
        self._sensordata.append(sensordata)

    def _get(self, sensor: str):
        return next((p for p in self._sensordata if p.sensor == sensor), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.commited = False
        self.sensordata = FakeRepository([])

    def _commit(self):
        self.commited = True

    def rollback(self):
        pass


class TestAddRawData:

    t0 = datetime.now()

    @pytest.mark.skip
    def test_for_new_sensordata(self):
        uow = FakeUnitOfWork()
        cmd = commands.CreateRawData(
            sensor="temperature",
            value=12,
            timestamp=self.t0,
        )
        messagebus.handle(cmd, uow)

        assert uow.sensordata.get("temperature") is not None
        assert uow.commited == True
