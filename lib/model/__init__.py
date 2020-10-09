from abc import abstractmethod

database_models = []


def DatabaseModel(cls):
    database_models.append(cls)


class DynamicModel:

    def __dict__(self):
        return self.data

    def __getattr__(self, key):
        if key in self.data:
            return self.data[key]

    def __setattr__(self, key, value):
        if key in self.data:
            self.data[key] = value


class HasRelationships:

    @abstractmethod
    def load_relationships(self):
        raise NotImplementedError

    @abstractmethod
    def relationship_fields(self):
        return []

    def __getstate__(self):
        state = self.__dict__.copy()
        fields_to_remove = self.relationship_fields()
        for field in fields_to_remove:
            try:
                del state[field]
            except KeyError:
                pass
        return state
