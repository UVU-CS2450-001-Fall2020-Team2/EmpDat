"""
Main entry into the application
"""

import tkinter as tk

import ui
from lib import *
from lib.model.employee import Employee
from lib.repository.db import database_setup
from lib.utils import sha_hash
from ui.control.login import LoginController


def boostrap_ui():
    ui.store.TK_ROOT = tk.Tk()
    ui.store.TK_ROOT.title('EmpDat')
    login_page = LoginController()
    ui.store.TK_ROOT.mainloop()


def cli():
    # TODO check for sys.argv, run command if given
    pass


def root_account_install():
    if Employee.read('root') is None:
        Employee.create(Employee({
            'id': 'root',
            'password': sha_hash(ROOT_DEFAULT_PASS),
            'last_name': 'Admin',
            'first_name': 'Root'
        }))


if __name__ == '__main__':
    database_setup({
        'DB_URL': DB_URL
    })
    root_account_install()
    cli()
    boostrap_ui()
