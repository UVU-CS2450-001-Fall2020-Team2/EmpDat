from tkinter.ttk import *


class EmployeePicker(OptionMenu):

    def __init__(self, master, variable, employees, default=None, **kwargs):
        self.choices = self._format_employees(employees)
        self.variable = variable

        if not default:
            default = self._employee_as_key(employees[0])

        super().__init__(master, variable, default, *self.choices, **kwargs)

    def get_value(self):
        return self.choices[self.variable.get()]

    @staticmethod
    def _format_employees(employees):
        employees.sort(key=lambda x: x.last_name)
        choices = {}
        for employee in employees:
            choices[EmployeePicker._employee_as_key(employee)] = employee.id
        return choices

    @staticmethod
    def _employee_as_key(employee):
        return f"{employee.first_name} {employee.last_name} ({employee.id})"
