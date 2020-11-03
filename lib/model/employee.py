"""
Employee Data Model
"""
import datetime

from sqlalchemy import MetaData, Table, Column, String

from lib.model import DynamicModel, HasRelationships, register_database_model
from lib.repository.db import DatabaseRepository
from lib.utils import sha_hash


@register_database_model
class Employee(DatabaseRepository, DynamicModel, HasRelationships):
    """
    Tied directly to the 'employee' table
    """
    resource_uri = 'employee'
    field_validators = {
        'id': 'notnull',
        'last_name': 'alpha',
        'first_name': 'alpha',
        # 'phone_number': 'phone',
        # 'emergency_contact_phone': 'phone'
    }
    field_casts = {
        'start_date': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        'date_of_birth': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
    }

    def __init__(self, data):
        DynamicModel.__init__(self, data)
        DatabaseRepository.__init__(self)

    def to_dict(self):
        return DynamicModel.to_dict(self)

    def load_relationships(self):
        pass

    def relationship_fields(self):
        return []

    @classmethod
    def authenticate(cls, username, password):
        employees = Employee.read_by(filters={
            'id': username
        })

        if len(employees) < 1:
            return None

        employee = employees[0]

        if sha_hash(password) == employee.password:
            return employee
        return None

    @classmethod
    def table(cls, metadata=MetaData()):
        return Table(cls.resource_uri, metadata,
                     Column('id', String(36), primary_key=True),
                     Column('last_name', String(36)),
                     Column('first_name', String(36)),
                     Column('password', String(255)),
                     extend_existing=True
                     )
