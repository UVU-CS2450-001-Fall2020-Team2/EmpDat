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
    def read(cls, model_id):
        """
        Read a single Model by it's ID
        :param model_id: model ID (must match to an 'id' column)
        :return: model
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
    def update(cls, model):
        """
        Uses the 'id' column to update the model
        :param model: model instance
        :return: model
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def destroy(cls, model_id):
        """
        Deletes the model from the data sink
        :param model_id: model's ID to destroy
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
