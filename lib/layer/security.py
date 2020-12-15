"""
Roles and Security Layer
"""

import dictdiffer

from lib.layer import Layer
from lib.model.change_request import ChangeRequest

CAN_CREATE = 'can_create'  # falsy. Base rule is to reject
CANT_READ = 'cant_read'  # truthy. Base rule is to allow. Deletes fields during read
CAN_UPDATE = 'can_update'  # falsy. Base rule is to reject
CAN_DESTROY = 'can_delete'  # falsy. Base rule is to reject
CAN_APPROVE = 'can_approve'  # falsy. Base rule is to reject
CAN = 'can'

ROLES = {
    "Admin": {
        CAN_CREATE: [
            "*"
        ],
        CAN_UPDATE: {
            "*"
        },
        CAN_DESTROY: [
            "*"
        ],
        CAN_APPROVE: {
            "*"
        }
    },
    "Accounting": {
        CAN_UPDATE: {
            "employee": [
                "salary",
                "hourly_rate",
                "commission_rate",
                "bank_routing",
                "bank_account",
                "classification_id",
                "paymethod_id",
                "role"
            ],
            "timesheet": [
                "*"
            ],
            "receipt": [
                "*"
            ]
        },
        CAN_CREATE: [
            "timesheet",
            "receipt"
        ],
        CAN: [
            "payroll",
        ]
    },
    "Reporter": {
        CANT_READ: {
            "employee": [
                "role",
                "social_security_number",
                "address_line1",
                "address_line2",
                "city",
                "state",
                "zipcode",
                "salary",
                "hourly_rate",
                "commission_rate",
                "bank_routing",
                "bank_account",
                "paymethod_id",
                "payment_method",  # view model field of the above
            ]
        },
        CAN_CREATE: [
            "timesheet",
            "receipt"
        ],
        CAN_UPDATE: {
            "timesheet": {
                "*"
            },
            "receipt": {
                "*"
            }
        }
    },
    "Viewer": {
        CANT_READ: {
            "employee": [
                "id",
                "role",
                "social_security_number",
                "start_date",
                "date_of_birth",
                "address_line1",
                "address_line2",
                "city",
                "state",
                "zipcode",
                "salary",
                "hourly_rate",
                "commission_rate",
                "bank_routing",
                "bank_account",
                "classification_id",
                "paymethod_id",
                "classification",  # view model field of the above
                "payment_method",  # view model field of the above
                'date_left',
                'notes'
            ]
        }
    }
}


class SecurityException(Exception):
    """
    Thrown when some security policy is violated
    """


class ChangeRequestException(Exception):
    """
    Thrown when a change request is entered instead of changing the data source directly
    """

    def __init__(self, message, *args, request=None):
        super().__init__(message, *args)
        self.request = request


class SecurityLayer(Layer):
    """
    Enforces role-based policies as outlined in ROLES
    """

    def __init__(self, user):
        super().__init__()

        if user.role not in ROLES:
            raise ValueError(f'No role programmed for role "{user.role}"')

        self.user_role_name = user.role
        self.user_role = ROLES[user.role]
        self.user = user

    @staticmethod
    def _get_model_name_from_repo_cls(repo_cls):
        return repo_cls.__name__.lower()

    def on_create(self, repo_cls, new_model):
        model_name = self._get_model_name_from_repo_cls(repo_cls)

        if model_name == 'changerequest':
            return

        if CAN_CREATE not in self.user_role:
            raise SecurityException(f'Creating {model_name} records is not allowed')

        if '*' in self.user_role[CAN_CREATE]:
            return

        if model_name not in self.user_role[CAN_CREATE]:
            raise SecurityException(f'Creating {model_name} records is not allowed')

        changes = list(dictdiffer.diff({}, new_model.to_dict()))

        # everyone who is not an Admin must request
        request = ChangeRequest({
            'author_user_id': self.user.id,
            'table_name': repo_cls.resource_uri,
            'row_id': None,
            'changes': ChangeRequest.serialize_dates(changes),
            'reason': 'No reason given'
        })
        request = ChangeRequest.create(request)
        raise ChangeRequestException('Request created successfully', request)

    def on_read_one(self, repo_cls, model):
        model_name = self._get_model_name_from_repo_cls(repo_cls)

        if CANT_READ not in self.user_role:
            return

        if '*' in self.user_role[CANT_READ]:
            raise SecurityException(f'Cannot read this {model_name}! '
                                    f'Insufficient permission.')

        if model_name in self.user_role[CANT_READ]:
            for field in self.user_role[CANT_READ][model_name]:
                if field == '*':
                    raise SecurityException(f'Cannot read this {model_name}! '
                                            f'Insufficient permission.')

                if hasattr(model, field):
                    delattr(model, field)

    def on_read_many(self, repo_cls, models):
        raise NotImplementedError('lib.repository._call_middlewares currently '
                                  'calls on_read_one iteratively')

    def on_update(self, repo_cls, updated_model, id_attr='id'):  # pylint: disable=too-many-branches
        """
        Uses dictdiffer to find the differences in the dictionary versions of the
        old and new model.

        If the following dictionaries were given:

        a_dict = {
            'a': 'foo',
            'b': 'bar',
            'd': 'barfoo'
        }

        b_dict = {
            'a': 'foo',
            'b': 'BAR',
            'c': 'foobar'
        }

        The dictdiffer tool would return the following:

        difference = list(dictdiffer.diff(a_dict, b_dict))
        print(difference)
            [
                ('change', 'b', ('bar', 'BAR')),
                ('add', '', [('c', 'foobar')]),
                ('remove', '', [('d', 'barfoo')])
            ]
        """
        model_name = self._get_model_name_from_repo_cls(repo_cls)

        if CAN_UPDATE not in self.user_role:
            raise SecurityException(f'Updating {model_name} records is not allowed')

        if '*' in self.user_role[CAN_UPDATE]:
            return

        if model_name not in self.user_role[CAN_UPDATE]:
            raise SecurityException(f'Updating {model_name} records is not allowed')

        # self.user_role[CAN_UPDATE][model_name] exists
        # now to look at the nitty-gritty of the changes...

        old_model = repo_cls.read(getattr(updated_model, repo_cls.id_attr))

        changes = list(dictdiffer.diff(old_model.to_dict(), updated_model.to_dict()))
        # print(changes)

        for action, field, values in changes:
            if action == 'add':
                print('Warning: attempt to add a field made. Was this desired?')
                for couple in values:
                    for key, ignored in couple:  # pylint: disable=unused-variable
                        if key not in self.user_role[CAN_UPDATE][model_name]:
                            raise SecurityException(f'Updating the {key} field in '
                                                    f'{model_name} records is not allowed')
            elif action == 'remove':
                for couple in values:
                    for key, ignored in couple:  # pylint: disable=unused-variable
                        if key not in self.user_role[CAN_UPDATE][model_name]:
                            raise SecurityException(f'Updating the {key} field in '
                                                    f'{model_name} records is not allowed')
            elif action == 'change':
                if field not in self.user_role[CAN_UPDATE][model_name]:
                    raise SecurityException(f'Updating the {field} field in '
                                            f'{model_name} records is not allowed')

        # everyone who is not an Admin must request
        request = ChangeRequest({
            'author_user_id': self.user.id,
            'table_name': repo_cls.resource_uri,
            'row_id': getattr(updated_model, id_attr),
            'changes': ChangeRequest.serialize_dates(changes),
            'reason': 'No reason given'
        })
        request = ChangeRequest.create(request)
        raise ChangeRequestException('Request created successfully', request)

    def on_destroy(self, repo_cls, model_id, id_attr='id'):
        model_name = self._get_model_name_from_repo_cls(repo_cls)

        if CAN_DESTROY not in self.user_role:
            raise SecurityException(f'Destroying {model_name} records is not allowed')

        if '*' in self.user_role[CAN_DESTROY]:
            return

        if model_name not in self.user_role[CAN_DESTROY]:
            raise SecurityException(f'Destroying {model_name} records is not allowed')

    def can_create(self, resource_uri):
        """
        Checks if user can create X

        :param resource_uri: X
        :return: True if can create X
        """
        if self.user_role and CAN_CREATE in self.user_role and '*' in self.user_role[CAN_UPDATE]:
            return True

        return self.user_role \
               and CAN_CREATE in self.user_role \
               and resource_uri in self.user_role[CAN_CREATE]

    def can_read(self, resource_uri, field):
        """
        Calculates if a role can access a certain field

        :param role: Role string
        :param resource_uri: URI str
        :param field: field name
        :return: bool if can read
        """

        return not (self.user_role
                    and CANT_READ in self.user_role
                    and resource_uri in self.user_role[CANT_READ]
                    and field in self.user_role[CANT_READ][resource_uri])

    def can_update(self, resource_uri):
        """
        Checks if user can update X

        :param resource_uri: X
        :return: True if can update X
        """
        if self.user_role and CAN_UPDATE in self.user_role and '*' in self.user_role[CAN_UPDATE]:
            return True

        return self.user_role \
               and CAN_UPDATE in self.user_role \
               and resource_uri in self.user_role[CAN_UPDATE]

    def can_(self, custom_operation: str):
        """
        Checks if an arbitrary operation can be done with this role

        :param custom_operation: operation string
        :return: bool if can do X
        """
        if self.user_role_name == 'Admin':
            return True

        return self.user_role and CAN in self.user_role \
               and custom_operation in self.user_role[CAN]
