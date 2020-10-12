import datetime

from sqlalchemy import MetaData, Table, Column, String

from lib.model import DynamicModel, HasRelationships, register_database_model
from lib.repository.db import DatabaseRepository


@register_database_model
class Employee(DynamicModel, DatabaseRepository, HasRelationships):
    resource_uri = 'employee'
    field_validators = {
        'last_name': 'alpha',
        'first_name': 'alpha',
        'phone_number': 'phone',
        'emergency_contact_phone': 'phone'
    }
    field_casts = {
        'start_date': datetime.date,
        'date_of_birth': datetime.date,
    }

    def __init__(self, data):
        super().__init__(data)
        DatabaseRepository().__init__()

    def load_relationships(self):
        pass

    def relationship_fields(self):
        return []

    @classmethod
    def table(cls, metadata=MetaData()):
        return Table(cls.resource_uri, metadata,
                     Column('id', String(36), primary_key=True),
                     Column('last_name', String(36)),
                     extend_existing=True
                     )
