from abc import abstractmethod

from sqlalchemy import create_engine, MetaData, select

from lib.repository import Repository
from lib.repository.validator import HasValidation


def database_setup(config):
    engine = create_engine(config['DB_URL'], echo=False)
    metadata = MetaData(engine)

    DatabaseRepository.engine = engine
    DatabaseRepository.url = config['DB_URL']
    DatabaseRepository.metadata = metadata

    from lib.model import database_models
    for model in database_models:
        model.table(metadata=metadata)
    metadata.create_all()


class DatabaseRepository(Repository, HasValidation):
    url: str
    metadata: MetaData

    def __init__(self):
        super().__init__()

    @classmethod
    def _open_connection(cls):
        return DatabaseRepository.engine.connect()

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def table(cls, metadata=MetaData()):
        """
        Table definition for the Repository

        WARNING: The id field must be named 'id'

        :param metadata: sqlalchemy MetaData object
        :return: sqlalchemy Table object
        """
        raise NotImplementedError

    @classmethod
    def create(cls, model):
        """
        Performs an INSERT

        :param model: instance
        :return: model instance
        """
        connection = cls._open_connection()
        statement = cls.table(DatabaseRepository.metadata).insert().values(**model.to_dict())
        connection.execute(statement)
        connection.close()
        return model

    @classmethod
    def read(cls, model_id):
        """
        Performs a SELECT * WHERE id = model_id given

        :param model_id:
        :return: model
        """
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = select([table]).where(table.c.id == model_id)
        result = connection.execute(statement)
        modelDict = result.fetchone() if result is not None else None
        connection.close()
        return type(cls)(modelDict) if modelDict is not None else None

    @classmethod
    def read_all(cls):
        """
        Performs a SELECT * on the entire table

        :return: all rows
        """
        connection = cls._open_connection()
        statement = select([cls.table(DatabaseRepository.metadata)])
        result = connection.execute(statement)
        modelDicts = result.fetchall() if result is not None else None
        connection.close()

        models = []
        if modelDicts is not None:
            for raw in modelDicts:
                models.append(type(cls)(raw))

        return models

    @classmethod
    def update(cls, model):
        """
        Performs an UPDATE <values> WHERE id = model_id query

        :param model: instance
        :return: model instance
        """
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = table.update().where(table.c.id == model.id).values(**model.to_dict())
        connection.execute(statement)
        connection.close()
        return model

    @classmethod
    def destroy(cls, model_id):
        """
        Performs a DELETE WHERE id = model_id query

        :param model_id: id only
        :return: None
        """
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = table.delete().where(table.c.id == model_id)
        connection.execute(statement)
        connection.close()
