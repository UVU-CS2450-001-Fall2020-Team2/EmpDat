from tkinter import *
from tkinter.ttk import *

from ui import store
from ui.window import *

COLUMN_CONFIG = {
    "id": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 13,)
        }
    },
    "name": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 14,)
        }
    },
    "address": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 13,)
        }
    },
    "city": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 13,)
        }
    },
    "state": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 13,)
        }
    },
    "zip": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 13,)
        }
    },
    "classification": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 13,)
        }
    },
    "pay_method": {
        "header": {
            'padx': 5,
            'pady': 2,
        },
        "body": {
            "font": ('Arial', 13,)
        }
    }
}


class DatabaseWindow(TkinterWindow):
    def __init__(self, event_handlers):
        super().__init__(event_handlers)
        database = self.master
        self.master.title('EmpDat')
        self.master.configure(bg='white')

        self.query_var = StringVar()
        self.query_var.trace("w", lambda name, index, mode, sv=self.query_var: self.event_handlers['query_change'](self.query_var.get()))

        self.results = {}
        self.edit_icon = PhotoImage(file="ui/icons/pencil.gif")
        self.delete_icon = PhotoImage(file="ui/icons/trash.gif")

        # This creates a tkinter variable needed for the dropdown list
        self.tkvar = StringVar(database)

        self.emp_dat = Label(database, text="Employee Database", font=('Arial', 30), anchor="center", background='white')
        self.search_label = Label(database, text="Search:", background='white')

        self.columns = {
            "id": Label(database, text="ID", background='white'),
            "name": Label(database, text="Name", background='white'),
            "address": Label(database, text="Address", background='white'),
            "city": Label(database, text="City", background='white'),
            "state": Label(database, text="State", background='white'),
            "zip": Label(database, text="Zip", background='white'),
            "classification": Label(database, text="Classification", background='white'),
            "pay_method": Label(database, text="Pay Method", background='white'),
        }
        self.current_user = Label(database, text=f"{store.AUTHENTICATED_USER.first_name} {store.AUTHENTICATED_USER.last_name}", font=('Arial', 15), anchor="center")

        # Create place to enter search query
        self.search_entry = Entry(database, textvariable=self.query_var)

        # new employee button
        self.new_employee = Button(database, text="New Employee"
                                   # ,command = self.add_employee (Call submit method to login user
                                   )

        # logout button
        self.logout = Button(database, text="Logout"
                             # ,command = self.logout (Call submit method to login user
                             )

    def setup_grid(self):
        # used grid method to arrange rows and columns
        # choices for filter dropdown
        choices = ('Filter', 'None', 'Pay', 'Department', 'Job Title', 'Last Name')
        self.dropdown = OptionMenu(self.master, self.tkvar, *choices)
        # Note: To find out which choice is currently selected in an OptionMenu widget,
        # the .get() method on the associated control variable will return that choice as a string.
        self.current_user.grid(row=0, column=7, sticky=NSEW, padx=5, pady=10, columnspan=4)
        self.emp_dat.grid(row=0, column=0, sticky=NSEW, padx=5, pady=10, columnspan=7, rowspan=2)
        self.logout.grid(row=1, column=7, sticky=NSEW, padx=5, pady=3, columnspan=4)
        self.search_label.grid(row=2, column=0, sticky=NSEW, pady=10, padx=5)
        # NSEW fills the whole column
        # padx and pady is padding horizontally (padx) or vertically (pady)
        self.search_entry.grid(row=2, column=1, sticky=NSEW, columnspan=6, padx=6, pady=10)
        self.dropdown.grid(row=2, column=6, sticky=NSEW, padx=6, pady=10)
        self.new_employee.grid(row=2, column=7, sticky=NSEW, columnspan=4, padx=5, pady=10)

        i = 0
        for key in self.columns:
            self.columns[key].grid(row=3, column=i, sticky=NSEW, **COLUMN_CONFIG[key]["header"])
            i += 1

    def add_to_result(self, to_add: dict):
        i = len(self.results) + 4
        row = []

        can_add = {x: to_add[x] for x in to_add if x in self.columns}

        j = 0
        for col, value in can_add.items():
            e = Label(self.master, width=10, text=value, background='white',
                      **COLUMN_CONFIG[col]["body"])
            e.grid(row=i, column=j)
            row.append(e)
            j += 1

        e = Button(self.master, text="Edit", image=self.edit_icon, command=lambda: self.on_edit(can_add['id']))
        e.grid(row=i, column=(len(self.columns) + 1))
        row.append(e)
        e = Button(self.master, text="Delete", image=self.delete_icon,
                   command=lambda: self.on_delete(can_add['id']))
        e.grid(row=i, column=(len(self.columns) + 2))
        row.append(e)

        self.results[can_add['id']] = row

    def destroy_results(self):
        for key in self.results:
            for row in self.results[key]:
                row.destroy()
        self.results = {}

    def on_edit(self, row_id):
        self.event_handlers['edit_employee'](row_id)

    def on_delete(self, row_id):
        self.destroy_row(row_id)
        # TODO call controller hook

    def destroy_row(self, row_id):
        for element in self.results[row_id]:
            element.destroy()


if __name__ == "__main__":
    db_page = DatabaseWindow({})
    db_page.setup_grid()
    db_page.mainloop()

# mainloop method will loop forever, waiting for events from the user, until the user exits the program –
# either by closing the window, or by terminating the program with a keyboard interrupt in the console.


"""Time spent: 
10/20: 2.5 hours 
10/26: 0.25 hours
"""
