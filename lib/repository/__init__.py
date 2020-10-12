from abc import abstractmethod


class Repository:

    @classmethod
    @abstractmethod
    def create(cls, model):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read(cls, id):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read_all(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, model):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def destroy(cls, id):
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def resource_uri(cls):
        raise NotImplementedError
