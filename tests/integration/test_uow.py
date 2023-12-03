from datetime import datetime, timedelta

from sqlalchemy import text
from sensorprocessor.service_layers import unit_of_work
from sensorprocessor.domain import model

from ..randomref import random_value

t0 = datetime.now() 

def insert_rawdata(sensor, value, timestamp, session, version_number=1):

    session.execute(text(
        "INSERT INTO sensordata (sensor, version_number) VALUES (:sensor, :version_number)"),
                    {"sensor": sensor, "version_number": version_number})

    session.execute(text(
        "INSERT INTO rawdata (sensor, value, timestamp) VALUES (:sensor, :value, :timestamp)"),
                    {"sensor": sensor, "value": value, "timestamp": timestamp})

    session.commit()

def get_rawdata_id(sensor, session):
    [rawdataid] = session.execute(text(
        "SELECT id FROM rawdata WHERE sensor = :sensor"), {"sensor": sensor}).scalars()
    return rawdataid

def test_uow_can_retrieve_sensordata(sqlite_session, sqlite_session_factory):
   
    value0 = random_value()
    insert_rawdata(sensor="temperature", value=value0, timestamp=t0, session=sqlite_session)
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    
    with uow:
        sensordata = uow.sensordata.get("temperature")

        assert sensordata.sensor == "temperature"
        assert sensordata.rawdata == [model.Rawdata("temperature", value0, t0)]


def test_uow_can_add_sensordata(sqlite_session, sqlite_session_factory):
    sensordata = model.Sensordata("temperature", 
                                  [model.Rawdata("temperature", random_value(), t0)])
    
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    with uow:
        uow.sensordata.add(sensordata)
        uow.commit()
    
    rawdata_id = get_rawdata_id(sensor="temperature", session=sqlite_session)
    
    assert rawdata_id == 1
