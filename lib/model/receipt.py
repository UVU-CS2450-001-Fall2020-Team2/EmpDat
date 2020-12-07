"""
Receipt Model
"""
from sqlalchemy import Table, MetaData, Column, String, \
    Integer, DateTime, Boolean, Float, BigInteger

from lib.model import DynamicModel, HasRelationships, register_database_model
from lib.repository.db import DatabaseRepository


@register_database_model
class Receipt(DatabaseRepository, DynamicModel, HasRelationships):
    """
    Receipt Model
    """
    resource_uri = 'receipt'
    field_validators = {

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

    @classmethod
    def table(cls, metadata=MetaData()) -> Table:
        return Table(cls.resource_uri, metadata,
                     Column('id', BigInteger().with_variant(Integer, "sqlite"), primary_key=True),
                     Column('user_id', String(36)),
                     Column('amount', Float),
                     Column('paid', Boolean, default=False),
                     Column('created_at', DateTime),
                     Column('modified_at', DateTime),
                     extend_existing=True
                     )
