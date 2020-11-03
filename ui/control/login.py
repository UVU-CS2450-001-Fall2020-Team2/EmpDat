from lib.model.employee import Employee
from ui.control import Controller
from ui.store import TK_ROOT
from ui.window.login import LoginWindow


class LoginController(Controller):

    def __init__(self):
        super().__init__(LoginWindow(TK_ROOT, {
            'submit': self.login
        }))

    def login(self, username, password):
        if Employee.authenticate(username, password) is not None:
            print('success!!')
