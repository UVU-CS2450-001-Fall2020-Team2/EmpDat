from ui.window.edit_employee import *


class NewEmployeeWindow(EditEmployeeWindow):
    def __init__(self, tk_root, event_handlers):
        super().__init__(tk_root, event_handlers)

        self.new_pg = self.master

        # Create place to enter search query
        self.search_entry = Entry(new_pg)

        # This creates a tkinter variable needed for the dropdown list
        self.tkvar = StringVar(new_pg)

        self.title = Label(new_pg, text="New Employee", font=(None, 30), anchor="center")
        self.general_info = Label(new_pg, text="General Information", font=(None, 17))
        self.id = Label(new_pg, text="ID")
        self.first_name_label = Label(new_pg, text="First Name", anchor="center")
        self.last_name_label = Label(new_pg, text="Last Name", anchor="center")
        self.address = Label(new_pg, text="Address", anchor="center")
        self.city = Label(new_pg, text="City", anchor="center")
        self.state = Label(new_pg, text="State", anchor="center")
        self.zip = Label(new_pg, text="Zip", anchor="center")
        self.employment_info = Label(new_pg, text="Employment Information", font=(None, 17))
        self.classification = Label(new_pg, text="Classification", anchor="center")
        self.pay_method = Label(new_pg, text="Pay Method", anchor="center")
        self.salary = Label(new_pg, text="Salary", anchor="center")
        self.hourly = Label(new_pg, text="Hourly", anchor="center")
        self.commission = Label(new_pg, text="Commission", anchor="center")
        self.id_entry = Entry(new_pg)
        self.first_name = Entry(new_pg)
        self.last_name = Entry(new_pg)
        self.address_entry = Entry(new_pg)
        self.city_entry = Entry(new_pg)
        self.state_entry = Entry(new_pg)
        self.zip_entry = Entry(new_pg)
        self.classification_entry = Entry(new_pg)
        # choices for filter dropdown
        self.choices = ('None', 'Hourly', 'Salary', 'Commission')
        self.pay_method_entry = OptionMenu(new_pg, self.tkvar, *self.choices)
        # Note: To find out which choice is currently selected in an OptionMenu widget,
        # the .get() method on the associated control variable will return that choice as a string.
        self.salary_entry = Entry(new_pg)
        self.hourly_entry = Entry(new_pg)
        self.commission_entry = Entry(new_pg)

        # Create Employee button
        self.submit = Button(new_pg, text="Create Employee",
                             # ,command = self.create_new (Call submit method to edit user
                             )

    def submit_button(self):
        """This is where the code for making a new employee will go. 
        This is overriding the same method in Edit Employee Class"""


if __name__ == "__main__":
    new_pg = Tk()
    new_pg.title("EmpDat")
    login_page = NewEmployeeWindow(new_pg, {})
    login_page.setup_grid()
    new_pg.mainloop()

# mainloop method will loop forever, waiting for events from the user, until the user exits the program –
# either by closing the window, or by terminating the program with a keyboard interrupt in the console.


"""Time spent: 
11/2: 2 hours
"""
