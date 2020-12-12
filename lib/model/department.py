"""
Department Model
"""
from sqlalchemy import Table, MetaData, Column, String, Integer

from lib.model import DynamicModel, HasRelationships
from lib.repository.db import DatabaseRepository


class Department(DatabaseRepository, DynamicModel, HasRelationships):
    """
    Department model. Unused at the moment
    """
    resource_uri = 'department'
    field_validators = {

    }
    field_optional_validators = {

    }
    field_casts = {

    }

    def to_dict(self):
        return self.trim_relationships(DynamicModel.to_dict(self))

    def load_relationships(self):
        pass

    def relationship_fields(self) -> list:
        return []

    @classmethod
    def new_empty(cls):
        raise NotImplementedError

    @classmethod
    def table(cls, metadata=MetaData()) -> Table:
        return Table(cls.resource_uri, metadata,
                     Column('department_id', Integer, primary_key=True, autoincrement=True),
                     Column('name', String(45)),
                     Column('head_emp_id', String(32)),
                     extend_existing=True
                     )
