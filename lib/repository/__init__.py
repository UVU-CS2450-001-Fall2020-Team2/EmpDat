"""
Repository types reside in this module
"""
from abc import abstractmethod

layers = []


def _call_layers(action, repo_cls, model_id=None, new_model=None, id_attr='id'):  # pylint: disable=too-many-branches
    """
    Utility method to call all layers

    Pylint: too-many-branches disabled because a dictionary dispatch system would not work here.
    :param action: str. Identifies what layer action to take
    :param repo_cls: The repository class where the action is done.
    :param model_id: Optional. ID desired
    :param new_model: Optional. If a new model is made or read, this is handed to the layer method
    :param id_attr: Optional. Name of ID attribute (default is 'id')
    :return: None
    """
    if model_id is not None and new_model is not None:
        raise ValueError('Either model_id or new_model needs to be specified!')

    if action == 'create':
        for layer in layers:
            layer.on_create(repo_cls, new_model)
        return
    if action == 'read_one':
        for layer in layers:
            layer.on_read_one(repo_cls, new_model)
        return
    if action == 'read_many':
        for model in new_model:
            for layer in layers:
                layer.on_read_one(repo_cls, model)
        return
    if action == 'update':
        for layer in layers:
            layer.on_update(repo_cls, new_model, id_attr=id_attr)
        return
    if action == 'destroy':
        for layer in layers:
            layer.on_destroy(repo_cls, model_id, id_attr=id_attr)
    else:
        raise ValueError('Invalid action specified')


class CanMutateData:
    """
    Attribute for Repositories that allow for data mutation after reading
    """

    @classmethod
    @abstractmethod
    def after_read(cls, model_read, id_attr='id'):
        """
        Called after a model is read
        :param model_read: the model object read from data source
        :param id_attr: name of ID attribute
        :return: raises Exception if interrupt is desired
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def after_read_many(cls, models_read, id_attr='id'):
        """
        Called after many models are read
        :param models_read: model objects read from data source
        :param id_attr: name of ID attribute
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
        _call_layers('create', cls, new_model=model)

    @classmethod
    @abstractmethod
    def read(cls, model_id, id_attr='id'):
        """
        Read a single Model by it's ID
        :param model_id: model ID
        :param id_attr: Optional. Name of ID attribute (default is 'id')
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
    def update(cls, model, id_attr='id'):
        """
        Uses the 'id' column to update the model
        :param model: model instance
        :param id_attr: Optional. Name of ID attribute (default is 'id')
        :return: model
        """
        _call_layers('update', cls, new_model=model, id_attr=id_attr)

    @classmethod
    @abstractmethod
    def destroy(cls, model_id, id_attr='id'):
        """
        Deletes the model from the data sink
        :param model_id: model's ID to destroy
        :param id_attr: Optional. Name of ID attribute (default is 'id')
        :return: None
        """
        _call_layers('destroy', cls, model_id=model_id, id_attr=id_attr)

    @classmethod
    def after_read(cls, model_read, id_attr='id'):
        _call_layers('read_one', cls, new_model=model_read, id_attr=id_attr)

    @classmethod
    def after_read_many(cls, models_read, id_attr='id'):
        _call_layers('read_many', cls, new_model=models_read)

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
