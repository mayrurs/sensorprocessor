import pytest 

from . import api_client

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_happy_path():
    
    api_client.post_to_add_rawdata("temperature", 12, "2023-12-03 12:00:00")
    api_client.post_to_add_rawdata("temperature", 15, "2023-12-03 12:00:01")
    api_client.post_to_add_rawdata("humidity", 100, "2023-12-03 12:00:01")

    r = api_client.get_current_value("temperature")

    assert r.status_code == 200
    assert {"sensor": "temperature", "value": 15} == r.json() 
