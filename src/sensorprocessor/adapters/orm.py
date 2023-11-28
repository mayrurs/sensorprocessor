import logging

from sqlalchemy.orm import registry, relationship
from sqlalchemy import (
        Table,
        Column, 
        String, 
        Integer,
        DateTime,
        ForeignKey,
        )

from sensorprocessor.domain import model

logger = logging.getLogger(__name__)
mapper_registry = registry()

rawdata = Table(
        "rawdata",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("sensor", ForeignKey("sensordata.sensor")),
        Column("value", Integer),
        Column("timestamp", DateTime)
        )

sensordata = Table(
        "sensordata", 
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("sensor", String),
         Column("version_number", Integer, nullable=False, server_default="0"),
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
            



