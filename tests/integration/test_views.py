from datetime import datetime, timedelta
from sensorprocessor import views
from sensorprocessor.domain import commands
from sensorprocessor.service_layers import unit_of_work, messagebus

t0 = datetime.now()

def test_current_value_view(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory=sqlite_session_factory)
    oldest = commands.CreateRawData(sensor="temperature", value=12, timestamp=t0)
    newer = commands.CreateRawData(sensor="temperature", value=13, timestamp=(t0 + timedelta(minutes=1)))
    newest = commands.CreateRawData(sensor="temperature", value=14, timestamp=(t0 + timedelta(minutes=2)))
    other = commands.CreateRawData(sensor="humidity", value=100, timestamp=(t0))
    messagebus.handle(oldest, uow)
    messagebus.handle(newer, uow)
    messagebus.handle(newest, uow)
    messagebus.handle(other, uow)

    assert views.get_current_value("temperature", uow) == newest.value
    

