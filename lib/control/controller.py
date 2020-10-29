from lib.model.employee import Employee
from exceptions.control_exceptions import SecurityException


class Controller(object):
    """
    docstring
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def create_employee(self, emp_name):
        try:
            self.model.create({"first_name": "John"})
            self.view.show_employee()
        except SecurityException as e:
            self.view.display_security_warning(emp_name, e)
