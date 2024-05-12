import pytest
from datetime import datetime, timedelta

from . import api_client


def datetime_to_str(datetime: datetime) -> str:
    return datetime.strftime(r"%Y-%m-%d %H:%M:%S")


t0 = datetime.now()
t0_str = datetime_to_str(t0)
t1_str = datetime_to_str(t0 + timedelta(minutes=1))


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_happy_path():

    api_client.post_to_add_rawdata("temperature", 12, t0_str)
    api_client.post_to_add_rawdata("temperature", 15, t1_str)
    api_client.post_to_add_rawdata("humidity", 100, t0_str)

    r = api_client.get_current_value("temperature")

    assert r.status_code == 200
    assert {"sensor": "temperature", "value": 15, "timestamp": t1_str} == r.json()
