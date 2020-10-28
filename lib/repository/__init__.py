"""
Repository types reside in this module
"""
from abc import abstractmethod

middlewares = []


def _call_middlewares(action, repo_cls, model_id=None, new_model=None, id_col='id'):
    """
    Utility method to call all middlewares
    :param action: str. Identifies what layer action to take
    :param repo_cls: The repository class where the action is done.
    :param model_id: Optional. ID desired
    :param new_model: Optional. If a new model is made or read, this is handed to the layer method
    :param id_col: Optional. Name of ID column identifier (default is 'id')
    :return: None
    """
    if model_id is not None and new_model is not None:
        raise ValueError('Either model_id or new_model needs to be specified!')

    if action == 'create':
        for middleware in middlewares:
            middleware.on_create(repo_cls, new_model)
        return
    if action == 'read_one':
        for middleware in middlewares:
            middleware.on_read_one(repo_cls, new_model)
        return
    if action == 'read_many':
        for model in new_model:
            for middleware in middlewares:
                middleware.on_read_one(repo_cls, model)
        return
    if action == 'update':
        for middleware in middlewares:
            middleware.on_update(repo_cls, new_model, id_col=id_col)
        return
    if action == 'destroy':
        for middleware in middlewares:
            middleware.on_destroy(repo_cls, model_id, id_col=id_col)
    else:
        raise ValueError('Invalid action specified')


class CanMutateData:

    @classmethod
    @abstractmethod
    def after_read(cls, model_read, id_col='id'):
        """
        Called after a model is read
        :param model_read: the model object read from data source
        :param id_col: name of ID column identifier
        :return: raises Exception if interrupt is desired
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def after_read_many(cls, models_read, id_col='id'):
        """
        Called after many models are read
        :param models_read: model objects read from data source
        :param id_col: name of ID column identifier
        :return: raises Exception if interrupt is desired
        """
        raise NotImplementedError


class Repository(CanMutateData):
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
        _call_middlewares('create', cls, new_model=model)

    @classmethod
    @abstractmethod
    def read(cls, model_id, id_col='id'):
        """
        Read a single Model by it's ID
        :param model_id: model ID (must match to an 'id' column)
        :param id_col: ID column identifier. (is it called 'id' or 'mymodel_id'?)
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
    def update(cls, model, id_col='id'):
        """
        Uses the 'id' column to update the model
        :param model: model instance
        :param id_col: ID column identifier. (is it called 'id' or 'mymodel_id'?)
        :return: model
        """
        _call_middlewares('update', cls, new_model=model, id_col=id_col)

    @classmethod
    @abstractmethod
    def destroy(cls, model_id, id_col='id'):
        """
        Deletes the model from the data sink
        :param model_id: model's ID to destroy
        :param id_col: ID column identifier. (is it called 'id' or 'mymodel_id'?)
        :return: None
        """
        _call_middlewares('destroy', cls, model_id=model_id, id_col=id_col)

    @classmethod
    def after_read(cls, model_read, id_col='id'):
        _call_middlewares('read_one', cls, new_model=model_read, id_col=id_col)

    @classmethod
    def after_read_many(cls, models_read, id_col='id'):
        _call_middlewares('read_many', cls, new_model=models_read)

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
        raise AttributeError('resource_uri: No resource URI set!')
