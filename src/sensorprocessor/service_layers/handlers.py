from sqlalchemy import text

from sensorprocessor.domain import model, events, commands
from sensorprocessor.service_layers import unit_of_work


def create_rawdata(cmd: commands.CreateRawData, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        sensordata = uow.sensordata.get(cmd.sensor)
        if sensordata is None:
            sensordata = model.Sensordata(sensor=cmd.sensor)
            uow.sensordata.add(sensordata)
        sensordata.add_raw_data(
            model.Rawdata(sensor=cmd.sensor, value=cmd.value, timestamp=cmd.timestamp)
        )
        uow.commit()


def publish_raw_data_creation(
    event: events.RawDataCreated,
    uow: unit_of_work.AbstractUnitOfWork,
):
    print(f"Raw data {event} created")


def add_newest_sensorvalue_to_read_model(
    event: events.Event,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            text(
                """
            INSERT INTO current_data_view (sensor, value, timestamp) 
            VALUES (:sensor, :value, :timestamp)        
            ON CONFLICT (sensor) DO UPDATE 
            SET value = :value, timestamp = :timestamp;"""
            ),
            {
                "sensor": event.sensor,
                "value": event.value,
                "timestamp": event.timestamp,
            },
        )
        uow.commit()


# ToDo: Can be removed
def clean_up_read_model(
    event: events.Event,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            text(
                "DELETE FROM current_data_view WHERE sensor = :sensor AND timestamp < :timestamp"
            ),
            {"sensor": event.sensor, "timestamp": event.timestamp},
        )
        uow.commit()
