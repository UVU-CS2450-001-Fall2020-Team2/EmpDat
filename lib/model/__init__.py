"""
Model base classes and traits
"""
from abc import abstractmethod, ABC

database_models = []


def register_database_model(cls):
    """
    A Class decorator that will automatically register a Model in the database schema
    :param cls: Class Type
    :return: None
    """
    database_models.append(cls)
    return cls


def find_model_by_name(model_name):
    """
    Returns model class by it's string class name if it has been previously registered
    See register_database_model
    :param model_name: str
    :return: Model class
    """
    for db_model in database_models:
        if db_model.__name__.lower() == model_name.lower():
            return db_model
    return None


class DynamicModel:
    """
    This Model attribute will allow fields to be completely dynamic

    reserved_keywords:
        Properties that become directly part of the object
        rather than part of the 'data' dict.
        Can be overridden.
    """
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
        self.cast_fields()

    def cast_fields(self):
        """
        Casts fields as specified in the field_casts dict. See also field_casts()

        Dictionary structure:
        {   [variable name]: [function doing conversion]  }

        Example:
            field_casts = {
                'id': lambda s: int(s),
                'salary': lambda s: float(s) if s is not None else None,
                'hourly_rate': lambda s: float(s) if s is not None else None,
                'commission_rate': lambda s: float(s) if s is not None else None,
            }
        :return: None
        """
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
        return None

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


class DynamicViewModel(DynamicModel, ABC):
    """
    Extends DynamicModel and adds view model conversion for presentation.

    View models are simple dictionaries.

    view_columns:
        This maps the database fields with it's prettier view

        Structure:
        {   [database field]: [what to display] }

        Example:
        {
            'id': 'ID',
            'social_security_number': 'SSN',
            'address_line1': 'Address'
        }
    """
    view_columns: dict = {}

    def __init__(self, data: dict):  # pylint: disable=useless-super-delegation
        """
        Only calls super constructor

        :param data: dict
        """
        super().__init__(data)

    def to_view_model(self):
        """
        Uses the view_columns dictionary and converts the model
        instance into a dictionary ready for presentation

        :return: view model dictionary
        """
        view_model = {}
        for key, value in self.view_columns.items():
            if getattr(self, key):
                view_model[value] = getattr(self, key)
        return view_model

    @classmethod
    def from_view_model(cls, view_model: dict):
        """
        Converts from a view model (preferably from the view) back to a model

        :param view_model: dictionary
        :return: Model
        """
        data = {}
        for key, value in cls.view_columns.items():
            if getattr(view_model, value):
                data[key] = view_model[value]

        return cls(data)


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
