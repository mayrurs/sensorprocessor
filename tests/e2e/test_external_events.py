import pytest
import json
import time
from datetime import datetime, timedelta
from tenacity import Retrying, RetryError, stop_after_delay

from . import redis_client, api_client


def datetime_to_str(datetime: datetime) -> str:
    return datetime.strftime(r"%Y-%m-%d %H:%M:%S")


t0 = datetime.now()
t0_str = datetime_to_str(t0)
t1_str = datetime_to_str(t0 + timedelta(minutes=1))


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
@pytest.mark.usefixtures("restart_redis_pubsub")
def test_add_raw_data_from_external_event():

    subscription = redis_client.subscribe_to("sensor_stream")

    # Previous current view
    api_client.post_to_add_rawdata("temperature", 12, t0_str)

    # Update view with external event
    redis_client.publish(
        "sensor_stream", {"sensor": "temperature", "value": 15, "timestamp": t1_str}
    )

    # wait until we see a message saying the order has been reallocated
    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
        with attempt:
            message = subscription.get_message(timeout=1)
            if message:
                messages.append(message)
            data = json.loads(messages[-1]["data"])
            assert data["sensor"] == "temperature"
            assert data["timestamp"] == t1_str
            time.sleep(1)

    # Todo Test against rawdata -> Test wheater externen events are added
    result = api_client.get_current_value("temperature")

    assert result.status_code == 200
    assert {
        "sensor": "temperature",
        "value": 15,
        "timestamp": t1_str,
    } == result.json()


# Todo test wheater view gets updated
