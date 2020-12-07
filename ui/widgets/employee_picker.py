"""
Employee picker for Tkinter
"""
from tkinter.ttk import OptionMenu


def _format_employees(employees):
    employees.sort(key=lambda x: x.last_name)
    choices = {}
    for employee in employees:
        choices[_employee_as_key(employee)] = employee.id
    return choices


def _employee_as_key(employee):
    return f"{employee.first_name} {employee.last_name} ({employee.id})"


class EmployeePicker(OptionMenu):  # pylint: disable=too-many-ancestors
    """
    Employee Picker that uses an OptionMenu
    """

    def __init__(self, master, variable, employees, default=None, **kwargs):
        self.choices = _format_employees(employees)
        self.variable = variable

        if not default:
            default = _employee_as_key(employees[0])

        super().__init__(master, variable, default, *self.choices, **kwargs)

    def get_value(self):
        """
        Gets value from selected item
        :return: value from selected item
        """
        return self.choices[self.variable.get()]
