"""
Repository types reside in this module
"""
from abc import abstractmethod


class Repository:
    """
    Base Repository Class for basic CRUD operations
    """

    @classmethod
    @abstractmethod
    def create(cls, model):
        """
        Creates the model in the data sink of choice
        :param model: instance with data
        :return: model
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read(cls, model_id, id_name='id'):
        """
        Read a single Model by it's ID
        :param model_id: model ID (must match to an 'id' column)
        :param id_name: ID identifier. (is it called 'id' or 'mymodel_id'?)
        :return: model
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read_by(cls, filters=None):
        """
        Reads all models that fit into the filters
        :return: list of models
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def read_all(cls):
        """
        Reads all models
        :return: list of models
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update(cls, model, id_name='id'):
        """
        Uses the 'id' column to update the model
        :param model: model instance
        :param id_name: ID identifier. (is it called 'id' or 'mymodel_id'?)
        :return: model
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def destroy(cls, model_id, id_name='id'):
        """
        Deletes the model from the data sink
        :param model_id: model's ID to destroy
        :param id_name: ID identifier. (is it called 'id' or 'mymodel_id'?)
        :return: None
        """
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def resource_uri(cls):
        """
        This is a helper to make the table/file/URI name more obvious.

        For example, the table() function in a DatabaseRepo should use
        this property to find the table name
        :return: Resource URI
        """
        raise NotImplementedError
