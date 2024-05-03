import logging

from sqlalchemy.orm import registry, relationship
from sqlalchemy import (
        Table,
        Column, 
        String, 
        Integer,
        DateTime,
        ForeignKey,
        UniqueConstraint,
        event
        )

from sensorprocessor.domain import model

logger = logging.getLogger(__name__)
mapper_registry = registry()

sensordata = Table(
        "sensordata", 
        mapper_registry.metadata,
        Column("sensor", String, primary_key=True),
        Column("version_number", Integer, nullable=False, server_default="0"),
         )

rawdata = Table(
        "rawdata",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("sensor", ForeignKey("sensordata.sensor")),
        Column("value", Integer),
        Column("timestamp", DateTime)
        )

current_data_view = Table(
        "current_data_view",
        mapper_registry.metadata,
        Column("id", Integer),
        Column("sensor", String, primary_key=True),
        Column("value", Integer),
        Column("timestamp", DateTime), 
        )

def start_mappers():
    logger.info("Starting mappers")
    mapper_rawdata = mapper_registry.map_imperatively(
            model.Rawdata,
            rawdata)

    mapper_registry.map_imperatively(
            model.Sensordata,
            sensordata,
            properties={"rawdata": relationship(mapper_rawdata)}
            )
            
@event.listens_for(model.Sensordata, "load")
def receive_load(sensordata, _):
    sensordata.events = []


