from tkinter import *
from tkinter.ttk import *

from ui.window import View


class DatabaseWindow(View):
    def __init__(self, tk_root, event_handlers):
        super().__init__(tk_root, event_handlers)

        # This creates a tkinter variable needed for the dropdown list
        self.tkvar = StringVar(database)

        self.database = self.master
        self.emp_dat = Label(database, text="Employee Database", font=(None, 30), anchor="center")
        self.search_label = Label(database, text="Search:")
        self.id = Label(database, text="ID")
        self.name = Label(database, text="Name")
        self.address = Label(database, text="Address")
        self.city = Label(database, text="City")
        self.state = Label(database, text="State")
        self.zip = Label(database, text="Zip")
        self.classification = Label(database, text="Classification")
        self.pay_method = Label(database, text="Pay Method")
        self.current_user = Label(database, text="Current User", font=(None, 15), anchor="center")

        # Create place to enter search query
        self.search_entry = Entry(database)

        # new employee button
        self.new_employee = Button(database, text="New Employee"
                                   # ,command = self.add_employee (Call submit method to login user
                                   )

        # logout button
        self.logout = Button(database, text="Logout"
                             # ,command = self.logout (Call submit method to login user
                             )

        self.setup_grid()

    def setup_grid(self):
        # used grid method to arrange rows and columns
        # choices for filter dropdown
        choices = ('Filter', 'None', 'Pay', 'Department', 'Job Title', 'Last Name')
        self.dropdown = OptionMenu(database, self.tkvar, *choices)
        # Note: To find out which choice is currently selected in an OptionMenu widget,
        # the .get() method on the associated control variable will return that choice as a string.
        self.current_user.grid(row=0, column=7, sticky=NSEW, padx=5, pady=10)
        self.emp_dat.grid(row=0, column=0, sticky=NSEW, padx=5, pady=10, columnspan=7, rowspan=2)
        self.logout.grid(row=1, column=7, sticky=NSEW, padx=5, pady=3, columnspan=2)
        self.search_label.grid(row=2, column=0, sticky=NSEW, pady=10, padx=5)
        # NSEW fills the whole column
        # padx and pady is padding horizontally (padx) or vertically (pady)
        self.search_entry.grid(row=2, column=1, sticky=NSEW, columnspan=5, padx=6, pady=10)
        self.dropdown.grid(row=2, column=6, sticky=NSEW, padx=6, pady=10)
        self.new_employee.grid(row=2, column=7, sticky=NSEW, padx=5, pady=10)
        self.id.grid(row=3, column=0, sticky=NSEW, pady=2, padx=5)
        self.name.grid(row=3, column=1, sticky=NSEW, pady=2, padx=5)
        self.address.grid(row=3, column=2, sticky=NSEW, pady=2, padx=5)
        self.city.grid(row=3, column=3, sticky=NSEW, pady=2, padx=5)
        self.state.grid(row=3, column=4, sticky=NSEW, pady=2, padx=5)
        self.zip.grid(row=3, column=5, sticky=NSEW, pady=2, padx=5)
        self.classification.grid(row=3, column=6, sticky=NSEW, pady=2, padx=5)
        self.pay_method.grid(row=3, column=7, sticky=NSEW, pady=2, padx=5)

    def add_employee(self):
        """This is where the code for adding a new employee will go"""
        # print("Added a new employee")

    def submit_logout(self):
        """This is where the code for logging out will go"""


if __name__ == "__main__":
    database = Tk()
    database.title("EmpDat")
    login_page = DatabaseWindow(database, {})
    login_page.setup_grid()
    database.mainloop()

# mainloop method will loop forever, waiting for events from the user, until the user exits the program –
# either by closing the window, or by terminating the program with a keyboard interrupt in the console.


"""Time spent: 
10/20: 2.5 hours 
10/26: 0.25 hours
"""
