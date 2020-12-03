from tkinter.ttk import *


class EmployeePicker(OptionMenu):

    def __init__(self, master, variable, employees, default=None, **kwargs):
        self.choices = self._format_employees(employees)

        super().__init__(master, variable, default, *self.choices, **kwargs)

    @staticmethod
    def _format_employees(employees):
        choices = {}
        for employee in employees:
            choices[f"{employee.first_name} {employee.last_name} ({employee.id})"] = employee.id
        return choices
