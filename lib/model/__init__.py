"""
Model base classes and traits
"""
from abc import abstractmethod

database_models = []


def register_database_model(cls):
    """
    A Class decorator that will automatically register a Model in the database schema
    :param cls: Class Type
    :return: None
    """
    database_models.append(cls)
    return cls


class ViewModel:
    def __init__(self):
        pass

    def to_view_model(self):
        return self.__dict__

    @classmethod
    def from_view_model(cls, view_model: dict):
        return cls(view_model)  # pylint: disable=too-many-function-args


class DynamicModel:
    """
    This Model attribute will allow fields to be completely dynamic
    """

    """
    Properties that become directly part of the object
    rather than part of the 'data' dict.
    Can be overridden.
    """  # pylint: disable=pointless-string-statement
    reserved_keywords = [
        'data',
        '_has_timestamps'
    ]


    def __init__(self, data: dict):
        """
        Sets dynamic data and casts fields as specified

        :param data: dict
        """
        self.data = data
        for field in self.field_casts:
            if field in self.data:
                self.data[field] = self.field_casts[field](self.data[field])

    @property
    def __dict__(self):
        return self.data

    def to_dict(self):
        """
        This is a helper in case this is used with the DatabaseRepository interface
        :return: data
        """
        return self.data

    def __getattr__(self, key):
        if key in self.reserved_keywords:
            return super().__getattribute__(key)
        if key in self.data:
            return self.data[key]
        raise AttributeError()

    def __setattr__(self, key, value):
        if key in self.reserved_keywords:
            super().__setattr__(key, value)
            return
        self.data[key] = value

    def __delattr__(self, key):
        if key in self.reserved_keywords:
            super().__delattr__(key)
            return
        del self.data[key]

    @property
    @classmethod
    @abstractmethod
    def field_casts(cls) -> dict:
        """
        Casts fields to a certain type using a given function
        when the model is created.
        It is recommended to set this as a class-wide variable.
        Must be a dictionary.

        Example:
        field_casts = {
            'date_of_birth': lambda x: datetime.date.fromtimestamp(x)
        }
        """
        raise NotImplementedError


class HasRelationships:
    """
    Helps with relational models
    """

    @abstractmethod
    def load_relationships(self):
        """
        This will eagerly load ALL relationships
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def relationship_fields(self) -> list:
        """
        :return: list of fields to strip on serialization
        """
        return []

    def __getstate__(self):
        """
        Strips relationship_fields on copying
        :return:
        """
        state = self.__dict__.copy()
        fields_to_remove = self.relationship_fields()
        for field in fields_to_remove:
            try:
                del state[field]
            except KeyError:
                pass
        return state

    def trim_relationships(self, data: dict):
        """
        Strips relationship_fields manually
        :return:
        """
        fields_to_remove = self.relationship_fields()
        for field in fields_to_remove:
            try:
                del data[field]
            except KeyError:
                pass
        return data
