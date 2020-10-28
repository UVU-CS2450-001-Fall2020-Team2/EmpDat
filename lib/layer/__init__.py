from abc import abstractmethod

from lib.repository import middlewares


class Layer:

    def __init__(self):
        middlewares.append(self)

    @abstractmethod
    def on_create(self, repo_cls, new_model):
        raise NotImplementedError

    @abstractmethod
    def on_read_one(self, repo_cls, model):
        raise NotImplementedError

    @abstractmethod
    def on_read_many(self, repo_cls, models):
        raise NotImplementedError

    @abstractmethod
    def on_update(self, repo_cls, new_model):
        raise NotImplementedError

    @abstractmethod
    def on_destroy(self, repo_cls, model_id, id_col='id'):
        raise NotImplementedError
