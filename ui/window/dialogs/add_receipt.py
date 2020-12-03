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
        self.employee_id = StringVar(self)
        self.employee_picker = EmployeePicker(self, self.employee_id, employees)
        self.employee_picker.grid(column=1, row=0)

        # Amount
        self.amount_lbl = Label(self, text="Total Sale:")
        self.amount_lbl.grid(column=0, row=1)
        self.amount = Entry(self)
        self.amount.grid(column=1, row=1)

        # Actions
        self.save_btn = Button(self, text="Save", command=lambda: self.event_handlers['save'](self))
        self.save_btn.grid(column=0, row=2)
        self.cancel_btn = Button(self, text="Cancel", command=lambda: self.destroy())
        self.cancel_btn.grid(column=1, row=2)
