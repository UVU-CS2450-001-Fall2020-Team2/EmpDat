from abc import abstractmethod

from sqlalchemy import create_engine, MetaData

from lib.model import database_models
from lib.repository.db import DatabaseRepository


def database_setup(config):
    engine = create_engine(config.get('root', 'DB_URL'), echo=False)
    metadata = MetaData(engine)

    DatabaseRepository.engine = engine
    DatabaseRepository.url = config.get('root', 'DB_URL')
    DatabaseRepository.metadata = metadata

    for model in database_models:
        model.table(metadata=metadata)
    metadata.create_all()


class Repository:

    @classmethod
    @abstractmethod
    def create(cls, model):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read(cls, id):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read_all(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, model):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def destroy(cls, id):
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def resource_uri(cls):
        raise NotImplementedError
