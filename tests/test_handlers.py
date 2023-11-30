from datetime import datetime
from re import A

from typing import List

from sensorprocessor.adapters import repository
from sensorprocessor.domain import events, commands, model
from sensorprocessor.service_layers import messagebus, unit_of_work

class FakeRepository(repository.AbstractSensorRepository):

    def __init__(self, sensordata: List =[]):
        self._sensordata = sensordata
        super().__init__()

    def _add(self, sensordata: model.Sensordata):
        self._sensordata.append(sensordata)

    def _get(self, sensor: str):
        return next(p for p in self._sensordata if p.sensor == sensor)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):

    def __init__(self):
        self.commited = False
        super().__init__()

    def __enter__(self):
        self.sensordata = FakeRepository([])
        super().__enter__()

    def _commit(self):
        self.commited = True

    def rollback(self):
        pass

class TestAddRawData:

    t0 = datetime.now()

    def test_for_new_product(self):
        breakpoint()
        uow = FakeUnitOfWork()
        cmd = commands.CreateRawData(
                sensor="temperature",
                value=12, 
                timestamp=self.t0,
                )
        messagebus.handle(cmd, uow)
        
        assert uow.sensordata.get("temperature") is not None
        assert uow.commited == True

