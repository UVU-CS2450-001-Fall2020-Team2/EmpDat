from tkinter import *
from tkinter.ttk import *

from lib.layer import security
from lib.model import employee
from ui import store
from ui.widgets.table import EmpDatTableCanvas
from ui.window import *


class DatabaseWindow(TkinterWindow):
    def __init__(self, event_handlers):
        super().__init__(event_handlers)

        self.results = {}
        self.edit_icon = PhotoImage(file="ui/icons/pencil.gif")
        self.delete_icon = PhotoImage(file="ui/icons/trash.gif")

        self.main = self.master
        self.main.geometry('1024x768')
        self.main.title('EmpDat')
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)
        self.table = EmpDatTableCanvas(f, col_modifiers={
            0: {  # ID
                'read_only': True
            },
            1: {  # Role
                'options': list(security.ROLES.keys())
            },
            8: {  # Classification
                'options': list(employee.classifications_dict.keys())
            },
            9: {  # Payment Method
                'options': list(employee.pay_methods_dict.keys())
            }
        }, on_unsaved=lambda x: self.set_save_state('normal' if not x else 'disabled'),
                                       on_selected=lambda: self.set_delete_state('normal'),
                                       data=self.results, rowheight=50)
        self.table.show()

        if store.AUTHENTICATED_USER.role == 'Viewer':
            self.table.read_only = True

        self.create_menu()
        self.create_bottom()

    def create_menu(self):
        # add menubar at the top
        self.menubar = Menu(self.main, tearoff=False)
        self.main.config(menu=self.menubar)
        # create the file object)
        self.filemenu = Menu(self.menubar, tearoff=False)
        # New Employee
        # adds a command to the menu option, calling it exit
        self.filemenu.add_command(label="New Employee", command=self.event_handlers['new_employee'])
        # Logout
        self.filemenu.add_command(label="Logout", command=self.event_handlers['file>logout'])
        # added "file" to our menu
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        # Reports Tab
        self.reports_menu = Menu(self.menubar, tearoff=False)
        self.reports_menu.add_command(label="Paylog", command=None)
        self.reports_menu.add_command(label="Employee Directory", command=None)
        self.menubar.add_cascade(label="Reports", menu=self.reports_menu)
        # Import tab
        self.import_menu = Menu(self.menubar, tearoff=False)
        self.import_menu.add_command(label="Employee", command=self.event_handlers['import>employees'])
        self.import_menu.add_command(label="Receipt", command=self.event_handlers['import>receipts'])
        self.import_menu.add_command(label="Timesheet", command=self.event_handlers['import>timesheets'])
        self.menubar.add_cascade(label="Import", menu=self.import_menu)
        #Add tab
        self.import_menu = Menu(self.menubar, tearoff=False)
        self.import_menu.add_command(label="New Receipt", command= self.event_handlers['add>receipts'])
        self.import_menu.add_command(label="New Time Sheet", command= self.event_handlers['add>timesheets'])
        self.menubar.add_cascade(label="Add", menu=self.import_menu)
        # Admin tab
        if store.AUTHENTICATED_USER.role == 'Admin':
            self.admin_menu = Menu(self.menubar, tearoff=False)
            self.admin_menu.add_command(label="Review Change Requests", command=self.event_handlers['admin>review'])
            self.menubar.add_cascade(label="Admin", menu=self.admin_menu)

    def create_bottom(self):
        buttons = Frame(self.main)

        self.new_button = Button(
            buttons,
            text="New",
            command=lambda: self.event_handlers['new_employee'],
        )
        self.search_button = Button(
            buttons,
            text="Search",
            command=lambda: self.table.showFilteringBar(),
        )
        self.delete_button = Button(
            buttons,
            text="Delete",
            state="disabled",
            command=self.event_handlers['delete'],
        )
        self.save_button = Button(
            buttons,
            text="Save",
            command=self.event_handlers['save'],
            state="disabled"
        )

        self.new_button.pack(side=LEFT, anchor=W)
        Label(buttons, text=f"({store.AUTHENTICATED_USER.first_name} {store.AUTHENTICATED_USER.last_name})").pack(
            side=LEFT, anchor=W)

        self.status = Label(buttons, text='')
        self.status.pack(side=LEFT, anchor=W)

        Frame(buttons, relief='flat', borderwidth=0).pack(fill=X, expand=1)

        self.save_button.pack(side=RIGHT, anchor=E)
        self.delete_button.pack(side=RIGHT, anchor=E)
        self.search_button.pack(side=RIGHT, anchor=E)

        buttons.pack(side=RIGHT, fill=X, expand=1)

    def set_save_state(self, state):
        self.save_button['state'] = state

    def set_delete_state(self, state):
        self.delete_button['state'] = state

    def new_employee(self):
        new_id = 12345
        self.add_to_result(new_id, {})
        self.table.movetoSelectedRow(recname=new_id)

    def add_to_result(self, id, to_add: dict):
        self.table.addRow(id, **to_add)

    def destroy_results(self):
        keys = list(self.table.model.data.keys())
        for key in keys:
            self.table.model.deleteRow(key=key)

    def on_edit(self, row_id):
        pass
        self.event_handlers['edit_employee'](row_id)

    def on_delete(self, row_id):
        pass
        self.destroy_row(row_id)
        # TODO call controller hook

    def destroy_row(self, row_id):
        del self.table.model.data[row_id]

    def set_status(self, text: str):
        self.status.configure(text=text)


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
