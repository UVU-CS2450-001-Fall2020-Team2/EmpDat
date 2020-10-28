"""
Roles and Security Layer
"""
from lib.layer import Layer

CAN_CREATE = 'can_create'  # falsy. Base rule is to reject
CANT_READ = 'cant_read'  # truthy. Base rule is to allow. Deletes fields during read
CAN_UPDATE = 'can_update'  # falsy. Base rule is to reject
CAN_DELETE = 'can_delete'  # falsy. Base rule is to reject
CAN_APPROVE = 'can_approve'  # falsy. Base rule is to reject

ROLES = {
    "Admin": {
        CAN_CREATE: [
            "*"
        ],
        CAN_UPDATE: {  # falsy. Base rule is to reject
            "*"
        },
        CAN_DELETE: [  # falsy. Base rule is to reject
            "*"
        ],
        CAN_APPROVE: {  # falsy. Base rule is to reject
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
        return repo_cls.__class__.__name__.lower().replace('repository', '')

    def on_create(self, repo_cls, new_model):
        model_name = self._get_model_name_from_repo_cls(repo_cls)
        if model_name not in self.user_role[CAN_CREATE]:
            raise SecurityException(f'Creating {model_name} records is not allowed')

    def on_read_one(self, repo_cls, model):
        model_name = self._get_model_name_from_repo_cls(repo_cls)
        if model_name in self.user_role[CANT_READ]:
            for field in self.user_role[CANT_READ][model_name]:
                if hasattr(model, field):
                    delattr(model, field)

    def on_read_many(self, repo_cls, models):
        raise NotImplementedError('lib.repository._call_middlewares currently '
                                  'calls on_read_one for every model read')

    def on_update(self, repo_cls, updated_model, id_attr='id'):
        old_model = repo_cls.read(getattr(updated_model, id_attr), id_attr=id_attr)

        # TODO do difference, check if it follows role policy

    def on_destroy(self, repo_cls, model_id, id_attr='id'):
        model_name = self._get_model_name_from_repo_cls(repo_cls)
        if model_name not in self.user_role['can_destory']:
            raise SecurityException(f'Destroying {model_name} records is not allowed')
