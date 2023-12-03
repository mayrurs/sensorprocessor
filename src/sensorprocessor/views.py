from sqlalchemy import text

from sensorprocessor.service_layers import unit_of_work

def get_current_value(sensor: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        value = uow.session.execute(text(
            "SELECT value FROM current_data_view WHERE sensor = :sensor"
            ), {"sensor": sensor}).scalars().first()
        return value





