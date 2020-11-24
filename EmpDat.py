"""
Main entry into the application
"""
import datetime

from lib import *
from lib.cli import dispatch_cmd
from lib.model.employee import Employee
from lib.repository.db import database_setup
from lib.utils import sha_hash
from ui.control.login import LoginController


def bootstrap_ui():
    LoginController().show()


def root_account_install():
    if Employee.read(-1) is None:
        Employee.create(Employee({
            'id': -1,
            'password': sha_hash(ROOT_DEFAULT_PASS),
            'role': 'Admin',
            'last_name': 'Admin',
            'first_name': 'Root',
            'user_group_id': 0,
            'start_date': datetime.date.today(),
            'date_of_birth': datetime.date.today(),
            'sex': -1,
            'address_line1': 'INVALID',
            'city': 'INVALID',
            'state': 'INVALID',
            'zipcode': '000',
            'classification_id': 0,
            'created_at': datetime.datetime.now(),
            'modified_at': datetime.datetime.now(),
            'date_left': datetime.date.today(),
            'notes': ''
        }))

if __name__ == '__main__':
    database_setup({
        'DB_URL': DB_URL
    })
    root_account_install()
    if not dispatch_cmd():
        bootstrap_ui()
