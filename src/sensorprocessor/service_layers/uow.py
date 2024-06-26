import abc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sensorprocessor import config
from sensorprocessor.adapters import repository


class AbstractUnitOfWork(abs.ABC):

    sensordata: repository.AbstractSensorRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def rollback():
        raise NotImplementedError

    @abc.abstractmethod
    def _commit():
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(config.get_postgres_uri(), isolation_level="REPEATABLE READ")
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.sensordata = repository.SqlAlchemySensorRepository(self.session)
        super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def commit(self):
        self.session.rollback()
