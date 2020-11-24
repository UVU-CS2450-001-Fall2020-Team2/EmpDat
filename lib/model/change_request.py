"""
Change Request Data Model
"""

from sqlalchemy import MetaData, Table, Column, String, DateTime, Text, BigInteger, JSON, Integer

from lib.model import DynamicModel, HasRelationships, register_database_model
from lib.model.employee import Employee
from lib.repository.db import DatabaseRepository


@register_database_model
class ChangeRequest(DatabaseRepository, DynamicModel, HasRelationships):
    """
    Tied directly to the 'change_request' table
    """
    resource_uri = 'change_request'
    field_validators = {
        'id': 'notnull',
        # 'phone_number': 'phone',
        # 'emergency_contact_phone': 'phone',
    }
    field_casts = {
    }

    def __init__(self, data):
        DynamicModel.__init__(self, data)
        DatabaseRepository.__init__(self)

        self.load_relationships()

    def to_dict(self):
        return self.trim_relationships(DynamicModel.to_dict(self))

    def load_relationships(self):
        self.author = Employee.read(self.author_user_id)
        try:
            self.approved_by = Employee.read(self.approved_by_user_id)
        except AttributeError:
            self.approved_by = None

    def relationship_fields(self):
        return [
            'author',
            'approved_by'
        ]

    def apply(self):
        pass

    @classmethod
    def table(cls, metadata=MetaData()):
        return Table(cls.resource_uri, metadata,
                     Column('id', BigInteger().with_variant(Integer, "sqlite"), primary_key=True),
                     Column('author_user_id', BigInteger),
                     Column('table_name', String(64)),
                     Column('row_id', BigInteger, nullable=True),
                     Column('changes', JSON),
                     Column('reason', Text, nullable=True),
                     Column('approved_at', DateTime, nullable=True),
                     Column('created_at', DateTime),
                     Column('modified_at', DateTime),
                     Column('approved_by_user_id', BigInteger, nullable=True),
                     extend_existing=True
                     )
