import pytest 
from sqlalchemy import text

from datetime import datetime, timedelta
from sensorprocessor import views
from sensorprocessor.domain import commands, model
from sensorprocessor.service_layers import unit_of_work, messagebus

def datetime_to_str(datetime: datetime) -> str:
    return datetime.strftime(r'%Y-%m-%d %H:%M:%S')

t0 = datetime.now()
t0_str = datetime_to_str(t0)
t1_str = datetime_to_str(t0 + timedelta(minutes=1))
t2_str = datetime_to_str(t0 + timedelta(minutes=2))


@pytest.mark.usefixtures("postgres_db") # Run against Postgres since SQL does not support Datetime operations
def test_current_value_view(postgres_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(postgres_session_factory)
    oldest = commands.CreateRawData(sensor="temperature", value=12, timestamp=t0_str)
    newer = commands.CreateRawData(sensor="temperature", value=13, timestamp=t1_str)
    newest = commands.CreateRawData(sensor="temperature", value=14, timestamp=t2_str)
    other = commands.CreateRawData(sensor="humidity", value=100, timestamp=t0_str)
    messagebus.handle(oldest, uow)
    messagebus.handle(newer, uow)
    messagebus.handle(newest, uow)
    messagebus.handle(other, uow)

    assert views.get_current_value("temperature", uow) == {"sensor": "temperature", "value": 14, "timestamp": t2_str}
    

