from sqlalchemy import MetaData

from lib.model import DynamicModel, HasRelationships, DatabaseModel
from lib.repository.db import DatabaseRepository


@DatabaseModel
class Employee(DynamicModel, DatabaseRepository, HasRelationships):

    def __init__(self, data):
        super().__init__(data)
        DatabaseRepository().__init__()

    def load_relationships(self):
        pass

    def relationship_fields(self):
        return []

    @classmethod
    def resource_uri(cls):
        return 'employee'

    @classmethod
    def table(cls, metadata=MetaData()):
        pass
