from os import wait
import requests

from sensorprocessor import config


def post_to_add_rawdata(sensor, value, timestamp):
    url = config.get_api_uri()
    r = requests.post(
        f"{url}/add_rawdata/",
        json={"sensor": sensor, "value": value, "timestamp": timestamp},
    )
    assert r.status_code == 201


def get_current_value(sensor):
    url = config.get_api_uri()
    return requests.get(f"{url}/get_current_value/{sensor}")
