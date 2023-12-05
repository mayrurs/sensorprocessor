import pytest

from sqlalchemy import text

from datetime import datetime, timedelta
from sensorprocessor.domain import model

t0 = datetime(2023, 11, 24, 7, 50, 40)
t1 = t0 + timedelta(minutes=1)

def test_can_add_to_database(sqlite_session):

    sensordata = model.Sensordata(sensor = "temperature",
                     rawdata= [
                         model.Rawdata("temperature", 12, t0),
                         model.Rawdata("temperature", 13, t1),
                        ]
                     )

    sqlite_session.add(sensordata)
    sqlite_session.commit()

    result = sqlite_session.execute(text( "SELECT * FROM rawdata")).all()
    expected = [
            (1, "temperature", 12, t0.strftime(r'%Y-%m-%d %H:%M:%S.%f')), 
            (2, "temperature", 13, t1.strftime(r'%Y-%m-%d %H:%M:%S.%f')),
                      ]
    assert result == expected


