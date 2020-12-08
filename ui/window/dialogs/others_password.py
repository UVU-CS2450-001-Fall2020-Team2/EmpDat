"""
View for changing others' passwords
"""
from tkinter import StringVar
from tkinter.ttk import Label, Entry, Button

from ui.widgets.employee_picker import EmployeePicker
from ui.window import TkinterDialog


class PasswordDialog(TkinterDialog):
    """
    Dialog for changing others' passwords
    """

    def __init__(self, event_handlers, employees):
        """
        Shows the employee picker, a password, and a password confirm field

        :param event_handlers: Expects 'save'
        :param employees: list of valid employees
        """
        super().__init__(event_handlers)

        # Employee Picker
        self.emp_label = Label(self, text="Employee:")
        self.emp_label.grid(column=0, row=0)
        self.employee_selected = StringVar(self)
        self.employee_picker = EmployeePicker(self, self.employee_selected, employees)
        self.employee_picker.grid(column=1, row=0)

        Label(self, text="New Password").grid(column=0, row=1)
        self.password_entry = Entry(self, width=50, show="•")
        self.password_entry.grid(column=1, row=1)

        Label(self, text="Confirm Password").grid(column=0, row=2)
        self.confirm_password_entry = Entry(self, width=50, show="•")
        self.confirm_password_entry.grid(column=1, row=2)

        Label(self, text="Passwords need to include one number, one "
                         "capital letter, and one special character") \
            .grid(column=0, row=3, columnspan=2)

        # Actions
        self.save_btn = Button(self, text="Save",
                               command=lambda: self.event_handlers['save'](
                                   self,
                                   self.employee_picker.get_value(),
                                   self.password_entry.get(),
                                   self.confirm_password_entry.get()
                               ))
        self.save_btn.grid(column=0, row=4)
        self.cancel_btn = Button(self, text="Cancel", command=self.destroy)
        self.cancel_btn.grid(column=1, row=4)

        self.master.bind('<Return>', lambda: self.event_handlers['save'](
            self,
            self.employee_picker.get_value(),
            self.password_entry.get(),
            self.confirm_password_entry.get()
        ))
