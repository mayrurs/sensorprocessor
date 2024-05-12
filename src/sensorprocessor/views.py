from sqlalchemy import text

from sensorprocessor.service_layers import unit_of_work


def get_current_value(sensor: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            text(
                "SELECT sensor, value, TO_CHAR(timestamp, 'YYYY-MM-DD HH24:MI:SS') AS timestamp FROM current_data_view WHERE sensor = :sensor ORDER BY timestamp ASC LIMIT 1"
            ),
            {"sensor": sensor},
        )
        result = [dict(r) for r in results.mappings()][0]
        return result


def sensordata(sensor, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            text("SELECT * FROM rawdata WHERE sensor = :sensor"), {"sensor": sensor}
        )
        return [dict(r) for r in results.mappings()]
