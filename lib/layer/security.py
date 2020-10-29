"""
Roles and Security Layer
"""
import dictdiffer

from lib.layer import Layer

CAN_CREATE = 'can_create'  # falsy. Base rule is to reject
CANT_READ = 'cant_read'  # truthy. Base rule is to allow. Deletes fields during read
CAN_UPDATE = 'can_update'  # falsy. Base rule is to reject
CAN_DESTROY = 'can_delete'  # falsy. Base rule is to reject
CAN_APPROVE = 'can_approve'  # falsy. Base rule is to reject

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
                "paymethod_id"
            ]
        },

    },
    "Reporter": {
        CANT_READ: {
            "employee": [
                "social_security_number"
            ]
        }
    },
    "Viewer": {
        CANT_READ: {
            "employee": [
                "social_security_number"
            ]
        }
    }
}


class SecurityException(Exception):
    """
    Thrown when some security policy is violated
    """


class SecurityLayer(Layer):
    """
    Enforces role-based policies as outlined in ROLES
    """

    def __init__(self, user_role_name):
        super().__init__()

        if user_role_name not in ROLES:
            raise ValueError(f'No role programmed for role "{user_role_name}"')

        self.user_role_name = user_role_name
        self.user_role = ROLES[user_role_name]

    @staticmethod
    def _get_model_name_from_repo_cls(repo_cls):
        return repo_cls.__name__.lower()

    def on_create(self, repo_cls, new_model):
        model_name = self._get_model_name_from_repo_cls(repo_cls)

        if CAN_CREATE not in self.user_role:
            raise SecurityException(f'Creating {model_name} records is not allowed')

        if '*' in self.user_role[CAN_CREATE]:
            return

        if model_name not in self.user_role[CAN_CREATE]:
            raise SecurityException(f'Creating {model_name} records is not allowed')

    def on_read_one(self, repo_cls, model):
        model_name = self._get_model_name_from_repo_cls(repo_cls)
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

        old_model = repo_cls.read(getattr(updated_model, id_attr), id_attr=id_attr)

        for action, field, values in \
                list(dictdiffer.diff(old_model.to_dict(), updated_model.to_dict())):
            if action == 'add':
                print('Warning: attempt to add a field made. Was this desired?')
                for couple in values:
                    for key, _ in couple:
                        if key not in self.user_role[CAN_UPDATE][model_name]:
                            raise SecurityException(f'Updating the {key} field in '
                                                    f'{model_name} records is not allowed')
            elif action == 'remove':
                for couple in values:
                    for key, _ in couple:
                        if key not in self.user_role[CAN_UPDATE][model_name]:
                            raise SecurityException(f'Updating the {key} field in '
                                                    f'{model_name} records is not allowed')
            elif action == 'change':
                if field not in self.user_role[CAN_UPDATE][model_name]:
                    raise SecurityException(f'Updating the {field} field in '
                                            f'{model_name} records is not allowed')

    def on_destroy(self, repo_cls, model_id, id_attr='id'):
        model_name = self._get_model_name_from_repo_cls(repo_cls)

        if CAN_DESTROY not in self.user_role:
            raise SecurityException(f'Destroying {model_name} records is not allowed')

        if '*' in self.user_role[CAN_DESTROY]:
            return

        if model_name not in self.user_role[CAN_DESTROY]:
            raise SecurityException(f'Destroying {model_name} records is not allowed')
