"""
View for Adding Timesheets
"""

from tkinter import StringVar, RIGHT, TOP, LEFT, BOTTOM
from tkinter.ttk import Label, Entry, Button, Frame

from tkcalendar import DateEntry

from ui.widgets.employee_picker import EmployeePicker
from ui.window import TkinterDialog


def _focus_next_widget(event) -> tuple:
    event.widget.tk_focusNext().focus()
    return ("break",)


class AddTimesheetDialog(TkinterDialog):  # pylint: disable=too-many-instance-attributes
    """
    Dialog for Adding Timesheets
    """

    def __init__(self, event_handlers, employees):
        """
        Shows:
            - employee
            - date
            - time in
            - time out

        :param event_handlers: Expects 'save'
        :param employees: list of valid employees
        """
        super().__init__(event_handlers)

        hour_validator = (
            self.register(self.hour_validator),
            '%d', '%s', '%S'  # action, val_before, char_to_change
        )
        minute_validator = (
            self.register(self.minute_validator),
            '%d', '%s', '%S'  # action, val_before, char_to_change
        )

        # Employee Picker
        self.frame1 = Frame(self)
        self.frame1.pack(side=TOP)
        self.emp_label = Label(self.frame1, text="Employee:")
        self.emp_label.pack(side=LEFT)
        self.employee_id = StringVar(self)
        self.employee_picker = EmployeePicker(self.frame1, self.employee_id, employees)
        self.employee_picker.pack(side=RIGHT)

        # Date picker
        self.frame2 = Frame(self)
        self.frame2.pack(side=TOP)
        self.date_lbl = Label(self.frame2, text='Date: ')
        self.date_lbl.pack(side=LEFT)
        self.cal = DateEntry(self.frame2, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
        self.cal.pack(side=RIGHT)

        # Clock In
        self.frame3 = Frame(self)
        self.frame3.pack(side=TOP)
        self.clock_in = Label(self.frame3, text="Time in: ")
        self.hour_1 = Entry(self.frame3, width=2, validate='key', validatecommand=hour_validator)
        self.hour_1.bind("<Tab>", _focus_next_widget)
        self.colon_1 = Label(self.frame3, text=':')
        self.min_1 = Entry(self.frame3, width=2, validate='key', validatecommand=minute_validator)
        self.min_1.bind("<Tab>", _focus_next_widget)
        self.clock_in.pack(side=LEFT)
        self.min_1.pack(side=RIGHT)
        self.colon_1.pack(side=RIGHT)
        self.hour_1.pack(side=RIGHT)

        # Clock Out
        self.frame4 = Frame(self)
        self.frame4.pack(side=TOP)
        self.clock_out = Label(self.frame4, text="Time out: ")
        self.hour_2 = Entry(self.frame4, width=2, validate='key', validatecommand=hour_validator)
        self.hour_2.bind("<Tab>", _focus_next_widget)
        self.colon_2 = Label(self.frame4, text=':')
        self.min_2 = Entry(self.frame4, width=2, validate='key', validatecommand=minute_validator)
        self.min_2.bind("<Tab>", _focus_next_widget)
        self.clock_out.pack(side=LEFT)
        self.min_2.pack(side=RIGHT)
        self.colon_2.pack(side=RIGHT)
        self.hour_2.pack(side=RIGHT)

        # Actions
        self.frame5 = Frame(self)
        self.frame5.pack(side=BOTTOM)
        self.save_btn = Button(self.frame5, text="Save",
                               command=lambda: self.event_handlers['save'](
                                   self,
                                   self.employee_picker.get_value(),
                                   self.cal.get_date(),
                                   self.hour_1.get(),
                                   self.min_1.get(),
                                   self.hour_2.get(),
                                   self.min_2.get(),
                               ))
        self.save_btn.pack(side=LEFT)
        self.cancel_btn = Button(self.frame5, text="Cancel", command=self.destroy)
        self.cancel_btn.pack(side=RIGHT)

        self.master.bind('<Return>', lambda: self.event_handlers['save'](
            self,
            self.employee_picker.get_value(),
            self.cal.get_date(),
            self.hour_1.get(),
            self.min_1.get(),
            self.hour_2.get(),
            self.min_2.get()
        ))

    def hour_validator(self, action: str, val_before: str, char_to_change: str):
        """
        Validates any hour field. See tkinter validators for more info

        :param action: 0 is deletion, 1 is addition, -1 is something else
        :param val_before: value before change
        :param char_to_change: character to add or delete
        :return: bool is_valid
        """
        if int(action) == 0:
            return True

        if len(val_before) + 1 > 2:
            self.bell()
            return False

        # Check for numbers
        if char_to_change in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:

            if int(val_before + char_to_change) > 23:
                self.bell()
                return False

            return True

        # Its wronnnngggg
        self.bell()  # .bell() plays that ding sound telling you there was invalid input
        return False

    def minute_validator(self, action: str, val_before: str, char_to_change: str):
        """
        Validates any minute field. See tkinter validators for more info

        :param action: 0 is deletion, 1 is addition, -1 is something else
        :param val_before: value before change
        :param char_to_change: character to add or delete
        :return: bool is_valid
        """
        if int(action) == 0:
            return True

        if len(val_before) + 1 > 2:
            self.bell()
            return False

        # Check for numbers
        if char_to_change in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:

            if int(val_before + char_to_change) > 59:
                self.bell()
                return False

            return True

        # Its wronnnngggg
        self.bell()  # .bell() plays that ding sound telling you there was invalid input
        return False
