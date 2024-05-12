import pytest

from datetime import datetime

from sqlalchemy import text

from sensorprocessor.domain import model
from sensorprocessor.adapters import repository

t0 = datetime(2023, 11, 24, 7, 50, 40)


def test_repository_can_add_sensordata(sqlite_session):

    repo = repository.SqlAlchemySensorRepository(sqlite_session)

    raw = model.Rawdata("temperature", 12, t0)
    sensordata = model.Sensordata(sensor="temperature", rawdata=[raw])
    repo.add(sensordata)
    repo.session.commit()

    result_sensordata = sqlite_session.execute(text("SELECT * FROM sensordata")).all()

    result_rawdata = sqlite_session.execute(text("SELECT * FROM rawdata")).all()

    assert result_sensordata == [("temperature", 0)]
    assert result_rawdata == [
        (1, "temperature", 12, t0.strftime(r"%Y-%m-%d %H:%M:%S.%f"))
    ]
