from sensorprocessor.domain import model, events, commands
from sensorprocessor.service_layers import unit_of_work

def create_rawdata(
        cmd: commands.CreateRawData,
        uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        sensordata = uow.sensordata.get(cmd.sensor)
        if sensordata is None:
            sensordata = model.Sensordata(sensor=cmd.sensor)
            uow.sensordata.add(sensordata)
        sensordata.rawdata.append(model.Rawdata(
                sensor=cmd.sensor,
                value=cmd.value, 
                timestamp=cmd.timestamp))
        uow.commit()

        sensordata.events.append(
                events.RawDataCreated(
                    cmd.sensor, 
                    cmd.value, 
                    cmd.timestamp
                    )
                )


def publish_raw_data_creation(
    event: events.RawDataCreated, 
    uow: unit_of_work.AbstractUnitOfWork,
    ):
    print(f"Raw data {event} created")
        
