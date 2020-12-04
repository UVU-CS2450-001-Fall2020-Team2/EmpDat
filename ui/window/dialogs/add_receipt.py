from tkinter import *
from tkinter.ttk import *

from ui.widgets.employee_picker import EmployeePicker
from ui.window import TkinterDialog


class AddReceiptDialog(TkinterDialog):

    def __init__(self, event_handlers, employees):
        super().__init__(event_handlers)

        # Employee Picker
        self.emp_label = Label(self, text="Employee:")
        self.emp_label.grid(column=0, row=0)
        self.employee_selected = StringVar(self)
        self.employee_picker = EmployeePicker(self, self.employee_selected, employees)
        self.employee_picker.grid(column=1, row=0)

        # Amount
        self.amount_lbl = Label(self, text="Total Sale:")
        self.amount_lbl.grid(column=0, row=1)
        validator = (self.register(self.validate), '%d', '%s', '%S')  # action, val_before, char_to_change
        self.amount = Entry(self, validate='key', validatecommand=validator, justify=RIGHT)
        self.amount.grid(column=1, row=1)

        # Actions
        self.save_btn = Button(self, text="Save",
                               command=lambda: self.event_handlers['save'](
                                   self,
                                   self.employee_picker.get_value(),
                                   self.amount.get()
                               )
                               )
        self.save_btn.grid(column=0, row=2)
        self.cancel_btn = Button(self, text="Cancel", command=lambda: self.destroy())
        self.cancel_btn.grid(column=1, row=2)

        self.master.bind('<Return>', lambda: self.event_handlers['save'](
            self,
            self.employee_picker.get_value(),
            self.amount.get()
        ))

    def validate(self, action: str, val_before: str, char_to_change: str):
        if int(action) == 0:
            return True

        # Check for numbers
        if char_to_change in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True

        # Do check if a . is in there
        if '.' not in val_before and char_to_change == '.':
            return True

        # Its wronnnngggg
        self.bell()  # .bell() plays that ding sound telling you there was invalid input
        return False
