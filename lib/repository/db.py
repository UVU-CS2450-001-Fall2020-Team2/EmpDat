from abc import abstractmethod

from sqlalchemy import MetaData, select

from lib.repository import Repository


class DatabaseRepository(Repository):
    url: str
    metadata: MetaData

    def __init__(self):
        super().__init__()

    @classmethod
    def _open_connection(cls):
        return DatabaseRepository.engine.connect()

    @property
    @classmethod
    @abstractmethod
    def table(cls, metadata=MetaData()):
        """
        Table definition for the Repository
        :param metadata: sqlalchemy MetaData object
        :return: sqlalchemy Table object
        """
        raise NotImplementedError

    @classmethod
    def create(cls, model):
        connection = cls._open_connection()
        statement = cls.table(DatabaseRepository.metadata).insert().values(**model.to_dict())
        connection.execute(statement)
        connection.close()
        return model

    # Args:
    #  - id - D-Tools ID
    @classmethod
    def read(cls, id):
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = select([table]).where(table.c.Id == id)
        result = connection.execute(statement)
        modelDict =  result.fetchone() if result is not None else None
        connection.close()
        return cls.from_dict(modelDict) if modelDict is not None else None

    @classmethod
    def read_all(cls):
        connection = cls._open_connection()
        statement = select([cls.table(DatabaseRepository.metadata)])
        result = connection.execute(statement)
        modelDicts =  result.fetchall() if result is not None else None
        connection.close()

        models = []
        if modelDicts is not None:
            for raw in modelDicts:
                models.append(cls.from_dict(raw))

        return models

    @classmethod
    def update(cls, model):
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = table.update().where(table.c.Id == model.Id).values(**model.to_dict())
        connection.execute(statement)
        connection.close()
        return model

    @classmethod
    def destroy(cls, id):
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = table.delete().where(table.c.Id == id)
        connection.execute(statement)
        connection.close()