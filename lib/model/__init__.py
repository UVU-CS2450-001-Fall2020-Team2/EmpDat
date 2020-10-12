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


class DynamicModel:
    """
    This Model attribute will allow fields to be completely dynamic
    """

    def __init__(self, data: dict):
        """
        Sets dynamic data and casts fields as specified

        :param data: dict
        """
        self.data = data
        for field in self.field_casts:
            if field in self.data:
                self.data[field] = type(self.field_casts[field])(self.data[field])

    def __dict__(self):
        return self.data

    def to_dict(self):
        return self.data

    def __getattr__(self, key):
        print('test!')
        if key in self.data:
            return self.data[key]

    def __setattr__(self, key, value):
        if key == 'data':
            return super().__setattr__(key, value)
        if key in self.data:
            self.data[key] = value

    @property
    @classmethod
    @abstractmethod
    def field_casts(cls) -> dict:
        """
        It is recommended to set this as a class-wide variable.
        Must be a dictionary.

        Example:
        field_casts = {
            'date_of_birth': datetime.date
        }
        """
        raise NotImplementedError


class HasRelationships:

    @abstractmethod
    def load_relationships(self):
        raise NotImplementedError

    @abstractmethod
    def relationship_fields(self) -> list:
        return []

    def __getstate__(self):
        print('----test!')
        state = self.__dict__.copy()
        fields_to_remove = self.relationship_fields()
        for field in fields_to_remove:
            try:
                del state[field]
            except KeyError:
                pass
        return state



