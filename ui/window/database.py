from tkinter import *
from tkinter.ttk import *

from tkintertable import TableCanvas

from ui import store
from ui.window import *


class DatabaseWindow(TkinterWindow):
    def __init__(self, event_handlers):
        super().__init__(event_handlers)
        self.master.title('EmpDat')

        self.results = {}
        self.edit_icon = PhotoImage(file="ui/icons/pencil.gif")
        self.delete_icon = PhotoImage(file="ui/icons/trash.gif")

        self.main = self.master
        self.main.geometry('800x500+200+100')
        self.main.title('EmpDat')
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)
        self.table = TableCanvas(f, data=self.results, rowheight=50)
        # table.importCSV('legacy/employees.csv')
        # print (table.model.columnNames)
        # table.model.data[1]['a'] = 'XX'
        # table.model.setValueAt('TESTCHANGE',0,0)
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
        self.filemenu.add_command(label="New Employee")
        # Logout
        self.filemenu.add_command(label="Logout", command=None)
        # added "file" to our menu
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        # Reports Tab
        self.reports_menu = Menu(self.menubar, tearoff=False)
        self.reports_menu.add_command(label="Paylog")
        self.reports_menu.add_command(label="Employee Directory")
        self.menubar.add_cascade(label="Reports", menu=self.reports_menu)
        # Import tab
        self.import_menu = Menu(self.menubar, tearoff=False)
        self.import_menu.add_command(label="Employee", command=None)
        self.import_menu.add_command(label="Receipt", command=None)
        self.import_menu.add_command(label="Timesheet", command=None)
        self.menubar.add_cascade(label="Import", menu=self.import_menu)

    def create_bottom(self):
        buttons = Frame(self.main)

        self.new_button = Button(
            buttons,
            text="New",
            command=lambda: self.add_to_result(12345, {}),
        )
        self.search_button = Button(
            buttons,
            text="Search",
            command=lambda: self.table.showFilteringBar(),
        )
        self.delete_button = Button(
            buttons,
            text="Delete",
            # command=lambda: event_handlers['submit'](self.entry.get(), self.password_entry.get()),
        )
        self.save_button = Button(
            buttons,
            text="Save",
            # command=lambda: event_handlers['submit'](self.entry.get(), self.password_entry.get()),
        )

        self.new_button.pack(side=LEFT, anchor=W)
        Label(buttons, text=f"({store.AUTHENTICATED_USER.first_name} {store.AUTHENTICATED_USER.last_name})").pack(side=LEFT, anchor=W)

        self.status = Label(buttons, text='')
        self.status.pack(side=LEFT, anchor=W)

        Frame(buttons, relief='flat', borderwidth=0).pack(fill=X, expand=1)

        self.save_button.pack(side=RIGHT, anchor=E)
        self.delete_button.pack(side=RIGHT, anchor=E)
        self.search_button.pack(side=RIGHT, anchor=E)

        buttons.pack(side=RIGHT, fill=X, expand=1)

    def new_employee(self):
        new_id = 12345
        self.add_to_result(new_id, {})
        self.table.movetoSelectedRow(recname=new_id)

    def add_to_result(self, id, to_add: dict):
        self.table.addRow(id, **to_add)
        print(self.table.model)

    def destroy_results(self):
        pass
        for key in self.results:
            for row in self.results[key]:
                self.results[key][row].destory()
        self.results = {}

    def on_edit(self, row_id):
        pass
        self.event_handlers['edit_employee'](row_id)

    def on_delete(self, row_id):
        pass
        self.destroy_row(row_id)
        # TODO call controller hook

    def destroy_row(self, row_id):
        pass
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
