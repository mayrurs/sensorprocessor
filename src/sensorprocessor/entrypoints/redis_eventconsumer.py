import json
import redis

import logger

from sensorprocessor import config
from sensorprocessor.adapters import orm
from sensorprocessor.domain import commands
from sensorprocessor.service_layer import messagebus, unit_of_work

r = redis.Redis(config.get_redis_host_and_port())
logging = logger.getLogger(__main__)

def main():
    orm.start_mappers()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("sensor_stream")

    for m in pubsub.listen():
        handle_create_rawdata(m)

def handle_create_rawdata(m):
    logging.debug(f"Handling {m}")
    data = json.loads(m["data"])
    cmd = commands.CreateRawData(data["sensor"], 
                                 data["value"],
                                 datetime.strptime(date["timestamp"], '%y-%m-%d %H:%M:%S')
                                 )
    messagebus.handle(cmd, uow=unit_of_work.SqlAlchemyUnitOfWork)


