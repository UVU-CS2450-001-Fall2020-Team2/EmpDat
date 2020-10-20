from sqlalchemy import Table, MetaData, Column, String, Integer, DateTime

from lib.model import DynamicModel, HasRelationships
from lib.repository.db import DatabaseRepository


class TimeSheet(DatabaseRepository, DynamicModel, HasRelationships):
    resource_uri = 'time_sheet'
    field_validators = {

    }
    field_casts = {

    }

    def to_dict(self):
        return DynamicModel.to_dict(self)

    def load_relationships(self):
        pass

    def relationship_fields(self) -> list:
        return []

    @classmethod
    def table(cls, metadata=MetaData()) -> Table:
        return Table(cls.resource_uri, metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True, sqlite_autoincrement=True),
                     Column('user_id', String(36)),
                     Column('datetime_begin', DateTime),
                     Column('datetime_end', DateTime),
                     Column('break_begin', DateTime),
                     Column('break_end', DateTime),
                     extend_existing=True
                     )
