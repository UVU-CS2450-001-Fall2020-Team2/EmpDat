"""
Database Repository with helper methods for setup
"""
import datetime
from abc import abstractmethod

from sqlalchemy import create_engine, MetaData, select, Table
from sqlalchemy.engine import Engine

from lib.model import database_models
from lib.repository import Repository
from lib.repository.validator import HasValidation


def database_setup(config):
    """
    This statically configures the ORM and database schema
    :param config: dict
    :return: None
    """
    DatabaseRepository.engine = create_engine(config['DB_URL'], echo=False)
    DatabaseRepository.url = config['DB_URL']
    DatabaseRepository.metadata = MetaData(DatabaseRepository.engine)

    for model in database_models:
        model.table(metadata=DatabaseRepository.metadata)
    DatabaseRepository.metadata.create_all()


class DatabaseRepository(Repository, HasValidation):
    """
    A SQL implementation of the Repository class
    """
    url: str
    metadata: MetaData
    engine: Engine

    def __init__(self, has_timestamps=True):
        Repository.__init__(self)

        self._has_timestamps = has_timestamps

        if has_timestamps and not getattr(self, 'created_at', None):
            self.created_at = datetime.datetime.now()
        if has_timestamps and not getattr(self, 'modified_at', None):
            self.modified_at = datetime.datetime.now()

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
        :param id_attr: Optional. Name of ID attribute (default is 'id'). Matches to column
        :return: model instance
        """
        cls.on_create(model)

        connection = cls._open_connection()
        statement = cls.table(DatabaseRepository.metadata).insert().values(**model.to_dict())
        result = connection.execute(statement)
        setattr(model, cls.id_attr, result.inserted_primary_key[0])
        connection.close()

        inserted = cls.read(getattr(model, cls.id_attr))

        return inserted

    @classmethod
    def read(cls, model_id):
        """
        Performs a SELECT * WHERE id = model_id given

        :param model_id: ID of model
        :param id_attr: Optional. Name of ID attribute (default is 'id'). Matches to column
        :return: model
        """
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = select([table]).where(table.c[cls.id_attr] == model_id)
        result = connection.execute(statement)

        # Converts the result proxy into a dictionary and an array of values only
        # data, values = {}, []
        data = {}
        rowcount = 0
        for rowproxy in result:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                data = {**data, **{column: value}}
            # values.append(data)
            rowcount += 1

        if rowcount > 0:
            model = cls(data)  # pylint: disable=too-many-function-args
        else:
            model = None

        connection.close()

        cls.after_read(model)

        return model

    @classmethod
    def read_by(cls, filters=None, as_dict=False):  # pylint: disable=arguments-differ
        """
        Performs a SELECT * WHERE filterKey (=) filterValue given

        :param filters: dictionary of fields and their filters
            Example:
                filters = {
                    'first_name': 'john_doe',                   # first_name = 'john_doe'
                    'age': [('>', 5)],                          # age > 5
                    'number_of_corn': [('>=', 5), ('<', 10)]    # 5 >= number_of_corn < 10
                }
        :param as_dict: Return results as dictionary with the `id_attr` as the key
        :return: all rows that fit filter criteria
        """
        if filters is None:
            return cls.read_all()

        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = select([table])

        for column, value in filters.items():
            if isinstance(value, list):
                statement = DatabaseRepository._convert_comparator(statement, table, column, value)
            else:
                statement = statement.where(table.c[column] == value)

        result = connection.execute(statement)
        model_dicts = result.fetchall() if result is not None else None
        connection.close()

        if as_dict:
            models = {}
            if model_dicts is not None:
                for raw in model_dicts:
                    models[raw[cls.id_attr]] = cls(dict(raw))  # pylint: disable=too-many-function-args

            cls.after_read_many(models_read=models.values())

            return models
        models = []
        if model_dicts is not None:
            for raw in model_dicts:
                models.append(cls(dict(raw)))  # pylint: disable=too-many-function-args

        cls.after_read_many(models_read=models)

        return models

    @classmethod
    def read_all(cls, as_dict=False):  # pylint: disable=arguments-differ
        """
        Performs a SELECT * on the entire table

        :param as_dict: Return results as dictionary with the `id_attr` as the key
        :return: all rows
        """
        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = select([table])
        result = connection.execute(statement)
        model_dicts = result.fetchall() if result is not None else None
        connection.close()

        if as_dict:
            models = {}
            if model_dicts is not None:
                for raw in model_dicts:
                    if raw[0] == -1:
                        continue
                    models[raw[cls.id_attr]] = cls(dict(raw))  # pylint: disable=too-many-function-args

            cls.after_read_many(models_read=models.values())

            return models
        models = []
        if model_dicts is not None:
            for raw in model_dicts:
                if raw[0] == -1:
                    continue
                models.append(cls(dict(raw)))  # pylint: disable=too-many-function-args

        cls.after_read_many(models_read=models)

        return models

    @classmethod
    def update(cls, model):
        """
        Performs an UPDATE <values> WHERE id = model_id query

        :param model: instance
        :param id_attr: Optional. Name of ID attribute (default is 'id'). Matches to column
        :return: model instance
        """
        cls.on_update(model)

        if model._has_timestamps:  # pylint: disable=protected-access
            model.modified_at = datetime.datetime.now()

        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = table.update().where(table.c[cls.id_attr] == model.id).values(**model.to_dict())
        connection.execute(statement)
        connection.close()
        return model

    @classmethod
    def destroy(cls, model_id):
        """
        Performs a DELETE WHERE id = model_id query

        :param model_id: id only
        :param id_attr: Optional. Name of ID attribute (default is 'id'). Matches to column
        :return: None
        """
        cls.on_destroy(model_id)

        connection = cls._open_connection()
        table = cls.table(DatabaseRepository.metadata)
        statement = table.delete().where(table.c[cls.id_attr] == model_id)
        connection.execute(statement)
        connection.close()

    @classmethod
    def run_statement(cls, statement):
        """
        Performs any statement given. Note that timestamps are
        NOT updated here nor are Layers called

        :param statement: can be created like the following:
            table = self.table(DatabaseRepository.metadata)
            statement = table.delete().where(...)
        :return: all rows of result set
        """
        connection = cls._open_connection()
        result = connection.execute(statement)
        results = result.fetchall() if result is not None else None
        connection.close()

        return results

    @classmethod
    def _convert_comparator(cls, statement, table, field, expressions):
        """
        Converts expressions like [('>', 5)] into x > 5 in a SQLAlchemy statement

        :param statement: statement to build upon
        :param expressions: an array of couples, the first being the comparator
            [(comparator, value})
                comparators should be strings
        :return: statement built
        """
        for expression in expressions:
            if len(expression) != 2:
                raise ValueError('DB Expressions should only have 1 comparator and 1 value')
            if expression[0] == '=':
                statement = statement.where(table.c[field] == expression[1])
            elif expression[0] == '!=':
                statement = statement.where(table.c[field] != expression[1])
            elif expression[0] == '>=':
                statement = statement.where(table.c[field] >= expression[1])
            elif expression[0] == '<=':
                statement = statement.where(table.c[field] <= expression[1])
            elif expression[0] == '>':
                statement = statement.where(table.c[field] > expression[1])
            elif expression[0] == '<':
                statement = statement.where(table.c[field] < expression[1])
            elif expression[0] == 'like':
                statement = statement.where(table.c[field].like(expression[1]))
            else:
                raise NotImplementedError('Invalid comparator given in DB Expression')
        return statement
