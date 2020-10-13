"""
Database Repository with helper methods for setup
"""
from abc import abstractmethod

from sqlalchemy import create_engine, MetaData, select, Table

from lib.model import database_models
from lib.repository import Repository
from lib.repository.validator import HasValidation


def database_setup(config):
    """
    This statically configures the ORM and database schema
    :param config: dict
    :return: None
    """
    engine = create_engine(config['DB_URL'], echo=False)
    metadata = MetaData(engine)

    DatabaseRepository.engine = engine
    DatabaseRepository.url = config['DB_URL']
    DatabaseRepository.metadata = metadata

    for model in database_models:
        model.table(metadata=metadata)
    metadata.create_all()


class DatabaseRepository(Repository, HasValidation):
    """
    A SQL implementation of the Repository class
    """
    url: str
    metadata: MetaData

    def __init__(self):
        Repository.__init__(self)

    @classmethod
    def _open_connection(cls):
        """
        Used by CRUD methods. This opens a connection with the database
        :return: connection instance
        """
        return DatabaseRepository.engine.connect()

    @abstractmethod
    def to_dict(self):
        """
        Used by CRUD methods. The model needs to define what is to be stored in the database
        :return: dict
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def table(cls, metadata=MetaData()) -> Table:
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

        # Converts the result proxy into a dictionary and an array of values only
        # data, values = {}, []
        data = {}
        for rowproxy in result:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                data = {**data, **{column: value}}
            # values.append(data)

        connection.close()
        return cls(data) if result is not None else None  # pylint: disable=too-many-function-args

    @classmethod
    def read_all(cls):
        """
        Performs a SELECT * on the entire table

        :return: all rows
        """
        connection = cls._open_connection()
        statement = select([cls.table(DatabaseRepository.metadata)])
        result = connection.execute(statement)
        model_dicts = result.fetchall() if result is not None else None
        connection.close()

        models = []
        if model_dicts is not None:
            for raw in model_dicts:
                models.append(cls(raw))  # pylint: disable=too-many-function-args

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
