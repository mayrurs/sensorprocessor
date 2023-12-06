import pytest 

from . import redis_client, api_client

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
@pytest.mark.usefixtures("restart_redis_pubsub")
def test_add_raw_data_from_external_event():

    redis_client.publish("sensor_stream", 
                         {"sensor": "temperature", 
                          "value": 14, 
                          "timestamp": "2023-12-01 12:00:00"}
                         )

    redis_client.publish("sensor_stream", 
                         {"sensor": "temperature", 
                          "value": 15, 
                          "timestamp": "2023-12-01 12:01:00"}
                         )

    r = api_client.get_current_value("temperature")

    assert r.status_code == 200
    assert {"sensor": "temperature", "value": 15} == r.json() 
