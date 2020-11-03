import ui
from lib.model.employee import Employee
from ui.control import Controller
from ui.control.database import DatabaseController
from ui.store import TK_ROOT
from ui.window.login import LoginWindow


class LoginController(Controller):

    def __init__(self):
        super().__init__(LoginWindow(TK_ROOT, {
            'submit': self.login
        }))

    def login(self, username, password):
        authenticated = Employee.authenticate(username, password)
        if authenticated is not None:
            ui.store.AUTHENTICATED_USER = authenticated
            print("Logged in as user ID", authenticated.id)
            # TODO send to main database page
            ui.open_window(DatabaseController)
        else:
            self.view.show_error(title='Error', message='Credentials incorrect!')
