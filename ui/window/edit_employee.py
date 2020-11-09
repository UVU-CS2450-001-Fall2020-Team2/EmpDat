from tkinter import *
from tkinter.ttk import *

from ui.window import TkinterWindow


# To Do:
# Make submit button bigger? THIS IS THE PRIORITY CURRENTLY


class EditEmployeeWindow(TkinterWindow):
    def __init__(self, event_handlers):
        super().__init__(event_handlers)
        self.master.title("EmpDat")

        edit_pg = self.master

        # Create place to enter search query
        self.search_entry = Entry(edit_pg)

        # This creates a tkinter variable needed for the dropdown list
        self.tkvar = StringVar(edit_pg)

        self.title = Label(edit_pg, text="Edit Employee", font=(None, 30), anchor="center")
        self.general_info = Label(edit_pg, text="General Information", font=('Arial', 17))
        self.id = Label(edit_pg, text="ID", anchor="center")
        self.first_name_label = Label(edit_pg, text="First Name", anchor="center")
        self.last_name_label = Label(edit_pg, text="Last Name", anchor="center")
        self.address = Label(edit_pg, text="Address", anchor="center")
        self.city = Label(edit_pg, text="City", anchor="center")
        self.state = Label(edit_pg, text="State", anchor="center")
        self.zip = Label(edit_pg, text="Zip", anchor="center")
        self.employment_info = Label(edit_pg, text="Employment Information", font=('Arial', 17))
        self.classification = Label(edit_pg, text="Classification", anchor="center")
        self.pay_method = Label(edit_pg, text="Pay Method", anchor="center")
        self.salary = Label(edit_pg, text="Salary", anchor="center")
        self.hourly = Label(edit_pg, text="Hourly", anchor="center")
        self.commission = Label(edit_pg, text="Commission", anchor="center")
        self.id_entry = Entry(edit_pg)
        self.first_name = Entry(edit_pg)
        self.last_name = Entry(edit_pg)
        self.address_entry = Entry(edit_pg)
        self.city_entry = Entry(edit_pg)
        self.state_entry = Entry(edit_pg)
        self.zip_entry = Entry(edit_pg)
        self.classification_entry = Entry(edit_pg)
        # choices for filter dropdown
        self.choices = ('None', 'Hourly', 'Salary', 'Commission')
        self.pay_method_entry = OptionMenu(edit_pg, self.tkvar, *self.choices)
        # Note: To find out which choice is currently selected in an OptionMenu widget,
        # the .get() method on the associated control variable will return that choice as a string.
        self.salary_entry = Entry(edit_pg)
        self.hourly_entry = Entry(edit_pg)
        self.commission_entry = Entry(edit_pg)

        # submit button
        self.submit = Button(edit_pg, text="Submit",
                             # ,command = self.submit_edit (Call submit method to edit user
                             )

    def setup_grid(self):
        # used grid method to arrange rows and columns
        # self.title = self.make_grid_entry('title',0,0,'NSEW',15, 10, 8, 2)
        self.title.grid(row=0, column=0, sticky=NSEW, padx=15, pady=10, columnspan=8, rowspan=2)
        self.general_info.grid(row=2, column=0, sticky=W, padx=15, pady=10, columnspan=8)
        # padx and pady is padding horizontally (padx) or vertically (pady)
        self.id.grid(row=4, column=0, sticky=NSEW, pady=2, padx=15)
        self.id_entry.grid(row=5, column=0, sticky=W, pady=2, padx=15)
        self.first_name_label.grid(row=4, column=1, sticky=NSEW, pady=2, padx=15)
        self.first_name.grid(row=5, column=1, sticky=W, pady=2, padx=15)
        self.last_name_label.grid(row=4, column=2, sticky=NSEW, pady=2, padx=15)
        self.last_name.grid(row=5, column=2, sticky=W, pady=2, padx=15)
        self.address.grid(row=6, column=0, sticky=NSEW, pady=2, padx=15)
        self.address_entry.grid(row=7, column=0, sticky=W, pady=2, padx=15)
        self.city.grid(row=6, column=1, sticky=NSEW, pady=2, padx=15)
        self.city_entry.grid(row=7, column=1, sticky=W, pady=2, padx=15)
        self.zip.grid(row=6, column=2, sticky=NSEW, pady=2, padx=15)
        self.zip_entry.grid(row=7, column=2, sticky=W, pady=2, padx=15)
        self.employment_info.grid(row=8, column=0, sticky=NSEW, pady=10, padx=15)
        self.classification.grid(row=9, column=0, sticky=NSEW, pady=2, padx=15)
        self.classification_entry.grid(row=10, column=0, sticky=W, pady=2, padx=15)
        self.pay_method.grid(row=9, column=1, sticky=NSEW, pady=2, padx=15)
        self.pay_method_entry.grid(row=10, column=1, sticky=NSEW, pady=2, padx=15)
        self.salary.grid(row=9, column=2, sticky=NSEW, pady=2, padx=15)
        self.salary_entry.grid(row=10, column=2, sticky=NSEW, pady=2, padx=15)
        self.hourly.grid(row=11, column=0, sticky=NSEW, pady=2, padx=15)
        self.hourly_entry.grid(row=12, column=0, sticky=W, pady=2, padx=15)
        self.commission.grid(row=11, column=1, sticky=NSEW, pady=2, padx=15)
        self.commission_entry.grid(row=12, column=1, sticky=W, pady=2, padx=15)
        self.submit.grid(row=14, column=1, sticky=NSEW, pady=15, padx=15, rowspan=2)

    # def make_grid_entry(self, tag, row, column, sticky_direction, horizontal_pad, vertical_pad, columspan, rowspan):
    #     return 'self.' + {} + '.grid(\'row = ' + {} + ',' + 'column = ' + {} + ', sticky = \
    #         ' + {} +', pady =' + {} + ', padx = ' + {} + '\
    #             columnspan = ' + {} + 'rowspan= ' + {}+ '\)'.format(
    #                 tag,row, column, sticky_direction,horizontal_pad, vertical_pad, columspan, rowspan)

    def submit_button(self):
        """This is where the code for editing an existing employee will go"""


if __name__ == "__main__":
    edit_pg = EditEmployeeWindow({})
    edit_pg.mainloop()

# mainloop method will loop forever, waiting for events from the user, until the user exits the program –
# either by closing the window, or by terminating the program with a keyboard interrupt in the console.


"""Time spent: 
10/27: 1.5 hours
11/2: 0.5 hours
"""
