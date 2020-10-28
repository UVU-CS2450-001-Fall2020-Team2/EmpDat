"""
Layer types reside in this module
"""

from abc import abstractmethod

from lib.repository import layers


class Layer:
    """
    A layer is anything that goes between a Repository and a Controller.
    Layers are useful for firing events and doing data mutations from CRUD operations.

    Methods are to return nothing and throw exceptions if conditions are not met
    """

    def __init__(self):
        layers.append(self)

    @abstractmethod
    def on_create(self, repo_cls, new_model):
        """
        Fired when Repository.create() is called.
        Called before model is created.

        :param repo_cls: Repository class type
        :param new_model: Model to be created
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def on_read_one(self, repo_cls, model):
        """
        Fired when Repository.read() is called.
        Called after a model is read.

        :param repo_cls: Repository class type
        :param model: Model that was read
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def on_read_many(self, repo_cls, models):
        """
        Fired when Repository.read_by() or Repository.read_all() are called.
        Called after models are read.

        :param repo_cls: Repository class type
        :param model: Models that was read
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def on_update(self, repo_cls, updated_model, id_attr='id'):
        """
        Fired when Repository.update() is called.
        Called before model is updated.

        :param repo_cls: Repository class type
        :param updated_model: Model to be updated
        :param id_attr: Name of ID attribute
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def on_destroy(self, repo_cls, model_id, id_attr='id'):
        """
        Fired when Repository.destroy() is called.
        Called before model is destroyed.

        :param repo_cls: Repository class type
        :param model_id: ID of model to be destroyed
        :param id_attr: Name of ID attribute
        :return: None
        """
        raise NotImplementedError
