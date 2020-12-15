"""
Change Request Data Model
"""
import datetime

from sqlalchemy import MetaData, Table, Column, String, \
    DateTime, Text, BigInteger, JSON, Integer

from lib.model import HasRelationships, register_database_model, \
    find_model_by_name, DynamicViewModel
from lib.model.employee import Employee
from lib.repository.db import DatabaseRepository


@register_database_model  # pylint: disable=too-many-ancestors
class ChangeRequest(DatabaseRepository, DynamicViewModel, HasRelationships):
    """
    Tied directly to the 'change_request' table
    """
    resource_uri = 'change_request'
    field_validators = {
        'id': 'notnull',
        # 'phone_number': 'phone',
        # 'emergency_contact_phone': 'phone',
    }
    field_optional_validators = {
    }
    field_casts = {
    }
    view_columns = {
        # 'id': 'ID',
        'author': 'Issued By',
        'table_name': 'Data Type',
        'row_id': 'ID affected',
        'changes': 'Changes',
        # 'reason': 'Reason',
        'created_at': 'Created On',
    }

    def __init__(self, data):
        DynamicViewModel.__init__(self, data)
        DatabaseRepository.__init__(self)

        self.load_relationships()

    def to_dict(self):
        return self.trim_relationships(DynamicViewModel.to_dict(self))

    def load_relationships(self):
        self.author = Employee.read(self.author_user_id)
        try:
            self.approved_by = Employee.read(self.approved_by_user_id)
        except AttributeError:
            self.approved_by = None

    def relationship_fields(self):
        return [
            'author',
            'approved_by'
        ]

    def apply_to_db(self, approved_by: Employee):
        """
        Only works for DatabaseRepository
        :param approved_by:
        :return:
        """
        model_cls = find_model_by_name(self.table_name)
        if not model_cls:
            raise Exception("Table name given in the ChangeRequest does not exist!")

        changes = ChangeRequest.deserialize_dates(self.changes)

        if self.row_id:  # is just a change?
            model = model_cls.read(self.row_id)
            for diff_type, field, values in changes:
                if diff_type == 'change':
                    setattr(model, field, values[1])
            model_cls.update(model)
        else:  # it must be an entire new object
            model_raw = {}
            for diff_type, field, values in changes:
                if diff_type == 'add':
                    for couple in values:
                        model_raw[couple[0]] = couple[1]
            model_cls.create(model_cls(model_raw))

        self.approved_by_user_id = approved_by.id  # pylint: disable=attribute-defined-outside-init
        self.approved_at = datetime.datetime.now()  # pylint: disable=attribute-defined-outside-init

        self.changes = ChangeRequest.serialize_dates(self.changes)

        ChangeRequest.update(self)

    @classmethod
    def new_empty(cls):
        raise NotImplementedError

    @classmethod
    def prettify_changes(cls, changes, model_name=None) -> str:
        """
        A utility for making changes prettier on the view

        :param changes: dictdiffer result
        :param model_name: model str
        :return: prettified changes
        """
        result = ""
        for diff_type, field, values in changes:  # pylint: disable=unused-variable
            if diff_type == 'change':
                if model_name:
                    model_cls = find_model_by_name(model_name)
                    result += f"{model_cls.view_columns[field]}: {values[0]} => {values[1]}\n"
                else:
                    result += f"{field}: {values[0]} > {values[1]}\n"
            else:
                for couple in values:
                    if model_name:
                        model_cls = find_model_by_name(model_name)
                        if couple[0] in model_cls.view_columns:
                            result += f"{model_cls.view_columns[couple[0]]}: {couple[1]}\n"
                        # else:
                        #     result += f"{model_cls.view_columns[couple[0]]}: {couple[1]}\n"
                    else:
                        result += f"{couple[0]}: {couple[1]}\n"
        return result.rstrip()

    @classmethod
    def table(cls, metadata=MetaData()) -> Table:
        return Table(cls.resource_uri, metadata,
                     Column('id', BigInteger().with_variant(Integer, "sqlite"), primary_key=True),
                     Column('author_user_id', BigInteger),
                     Column('table_name', String(64)),
                     Column('row_id', BigInteger, nullable=True),
                     Column('changes', JSON),
                     Column('reason', Text, nullable=True),
                     Column('approved_at', DateTime, nullable=True),
                     Column('created_at', DateTime),
                     Column('modified_at', DateTime),
                     Column('approved_by_user_id', BigInteger, nullable=True),
                     extend_existing=True
                     )

    @staticmethod
    def serialize_dates(changes):
        for action, field, values in changes:
            if action == 'add':
                for i in range(len(values)):
                    couple = values[i]
                    mutable = list(couple)
                    if isinstance(couple[1], datetime.datetime):
                        mutable[1] = couple[1].isoformat()
                    values[i] = tuple(mutable)

        return changes

    @staticmethod
    def deserialize_dates(changes):
        for action, field, values in changes:
            if action == 'add':
                for i in range(len(values)):
                    couple = values[i]
                    mutable = list(couple)
                    try:
                        mutable[1] = datetime.datetime.strptime(couple[1], "%Y-%m-%dT%H:%M:%S")
                        values[i] = tuple(mutable)
                    except:
                        try:
                            mutable[1] = datetime.datetime.strptime(couple[1], "%Y-%m-%dT%H:%M:%S.%f")
                            values[i] = tuple(mutable)
                        except:
                            continue
        return changes
