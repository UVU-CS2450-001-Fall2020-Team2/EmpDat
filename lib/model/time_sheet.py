"""
Timesheet Model
"""
from sqlalchemy import Table, MetaData, Column, String, Integer, DateTime, Boolean, BigInteger

from lib.model import DynamicModel, HasRelationships, register_database_model
from lib.repository.db import DatabaseRepository


@register_database_model
class TimeSheet(DatabaseRepository, DynamicModel, HasRelationships):
    """
    Timesheet Model
    """
    resource_uri = 'time_sheet'
    field_validators = {

    }
    field_optional_validators = {

    }
    field_casts = {

    }

    def __init__(self, data):
        DynamicModel.__init__(self, data)
        DatabaseRepository.__init__(self)

    def to_dict(self):
        return self.trim_relationships(DynamicModel.to_dict(self))

    def load_relationships(self):
        pass

    def relationship_fields(self) -> list:
        return []

    def to_hours(self):
        """
        Converts timestamps to time in hours
        :return: float
        """
        difference = self.datetime_end - self.datetime_begin
        return difference.total_seconds() / 3600  # seconds to hour

    @classmethod
    def new_empty(cls):
        raise NotImplementedError

    @classmethod
    def table(cls, metadata=MetaData()) -> Table:
        return Table(cls.resource_uri, metadata,
                     Column('id', BigInteger().with_variant(Integer, "sqlite"), primary_key=True),
                     Column('user_id', String(36)),
                     Column('datetime_begin', DateTime),
                     Column('datetime_end', DateTime),
                     Column('break_begin', DateTime, nullable=True),
                     Column('break_end', DateTime, nullable=True),
                     Column('paid', Boolean, default=False),
                     Column('created_at', DateTime),
                     Column('modified_at', DateTime),
                     extend_existing=True
                     )
