import pytest 
import json
from tenacity import Retrying, RetryError, stop_after_delay

from . import redis_client, api_client

@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
@pytest.mark.usefixtures("restart_redis_pubsub")
def test_add_raw_data_from_external_event():
    
    subscription = redis_client.subscribe_to("sensor_stream")

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

     # wait until we see a message saying the order has been reallocated
    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
        with attempt:
            message = subscription.get_message(timeout=1)
            if message:
                messages.append(message)
                print(messages)
            data = json.loads(messages[-1]["data"])
            assert data["sensor"] == "temperature"
            assert data["timestamp"] == "2023-12-01 12:00:00"

    r = api_client.get_current_value("temperature")

    assert r.status_code == 200
    assert {"sensor": "temperature", "value": 15} == r.json() 