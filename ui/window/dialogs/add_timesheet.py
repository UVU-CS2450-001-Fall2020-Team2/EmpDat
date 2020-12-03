from tkinter import *
from tkinter.ttk import *

from tkcalendar import DateEntry

from ui.widgets.employee_picker import EmployeePicker
from ui.window import TkinterDialog


class AddTimesheetDialog(TkinterDialog):

    def __init__(self, event_handlers, employees):
        super().__init__(event_handlers)

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
        self.hour_1 = Entry(self.frame3, width=2)
        self.colon_1 = Label(self.frame3, text=':')
        self.min_1 = Entry(self.frame3, width=2)
        self.clock_in.pack(side=LEFT)
        self.hour_1.pack(side=RIGHT)
        self.colon_1.pack(side=RIGHT)
        self.min_1.pack(side=RIGHT)

        # Clock Out
        self.frame4 = Frame(self)
        self.frame4.pack(side=TOP)
        self.clock_out = Label(self.frame4, text="Time out: ")
        self.hour_2 = Entry(self.frame4, width=2)
        self.colon_2 = Label(self.frame4, text=':')
        self.min_2 = Entry(self.frame4, width=2)
        self.clock_out.pack(side=LEFT)
        self.hour_2.pack(side=RIGHT)
        self.colon_2.pack(side=RIGHT)
        self.min_2.pack(side=RIGHT)

        # Actions
        self.frame5 = Frame(self)
        self.frame5.pack(side=BOTTOM)
        self.save_btn = Button(self.frame5, text="Save", command=lambda: self.event_handlers['save'](self))
        self.save_btn.pack(side=LEFT)
        self.cancel_btn = Button(self.frame5, text="Cancel", command=self.destroy)
        self.cancel_btn.pack(side=RIGHT)

