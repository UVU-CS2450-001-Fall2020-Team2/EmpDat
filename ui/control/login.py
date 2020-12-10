"""
Login Controller class
"""

from lib.layer.security import SecurityLayer
from lib.model.employee import Employee
from ui import store
from ui.control import Controller
from ui.control.database import DatabaseController
from ui.window.login import LoginWindow


class LoginController(Controller):
    """
    Manages login
    """

    def __init__(self):
        """
        Uses Login Window
        """
        super().__init__(LoginWindow({
            'submit': self.login
        }))

    def login(self, username, password):
        """
        If authentication is successful, the database window is spawned

        :param username: str
        :param password: str
        :return: None
        """
        if not self.view.validate():
            return

        try:
            int(username)
        except ValueError as e:
            self.view.show_error('Invalid Employee ID', 'Please ensure your ID is entered in correctly.')
            return

        authenticated = Employee.authenticate(username, password)
        if authenticated is not None:
            store.AUTHENTICATED_USER = authenticated
            SecurityLayer(authenticated)
            print("Logged in as user ID", authenticated.id)
            self.view.destroy()
            DatabaseController().show()
        else:
            self.view.show_error(title='Error', message='Credentials incorrect!')
