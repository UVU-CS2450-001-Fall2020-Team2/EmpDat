"""
Employee Data Model
"""

from sqlalchemy import MetaData, Table, Column, String, DateTime, Float, Integer, Text, Date, BigInteger

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
        # 'emergency_contact_phone': 'phone',
    }
    field_casts = {
        # 'start_date': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'date_of_birth': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'date_left': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'created_at': lambda d: datetime.datetime.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'modified_at': lambda d: datetime.datetime.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
    }

    def __init__(self, data):
        DynamicModel.__init__(self, data)
        DatabaseRepository.__init__(self)

    def to_dict(self):
        return self.trim_relationships(DynamicModel.to_dict(self))

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
                     Column('id', BigInteger().with_variant(Integer, "sqlite"), primary_key=True),
                     Column('password', String(255)),
                     Column('social_security_number', String(12)),
                     Column('user_group_id', Integer),
                     Column('department_id', Integer),
                     Column('role', String(64)),
                     Column('last_name', String(64)),
                     Column('first_name', String(64)),
                     Column('start_date', Date),
                     Column('date_of_birth', Date),
                     Column('sex', Integer),
                     Column('address_line1', String(128)),
                     Column('address_line2', String(128), nullable=True),
                     Column('city', String(45)),
                     Column('state', String(45)),
                     Column('zipcode', String(16)),
                     Column('email', String(45), nullable=True),
                     Column('phone_number', String(45), nullable=True),
                     Column('emergency_contact_name', String(45), nullable=True),
                     Column('emergency_contact_relation', String(45), nullable=True),
                     Column('emergency_contact_phone', String(45), nullable=True),
                     Column('classification_id', Integer),
                     Column('paymethod_id', Integer),
                     Column('salary', Float, nullable=True),
                     Column('hourly_rate', Float, nullable=True),
                     Column('commission_rate', Float, nullable=True),
                     Column('bank_routing', String(32), nullable=True),
                     Column('bank_account', String(32), nullable=True),
                     Column('timesheet', Float, nullable=True),
                     Column('created_at', DateTime),
                     Column('modified_at', DateTime),
                     Column('date_left', Date, nullable=True),
                     Column('notes', Text, nullable=True),
                     extend_existing=True
                     )
