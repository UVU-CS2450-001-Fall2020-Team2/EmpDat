from tkinter import *

from tkintertable import TableCanvas
from ttkthemes import ThemedStyle

data = {'rec1': {'firstName': 'John', 'lastName': 'Doe', 'classification': 'salary'},
       'rec2': {'firstName': 'Suzie', 'lastName': 'Johnson', 'classification': 'salary'},
       'rec3': {'firstName': 'Phil', 'lastName': 'Harris', 'classification': 'salary'}
       }

# from tkintertable.Testing import sampledata
# data=sampledata()
#print(data)

class TestApp(Frame):
    """Basic test frame for the table"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ThemedStyle(self)
        style.theme_use('arc')

        self.main = self.master
        self.main.geometry('800x500+200+100')
        self.main.title('EmpDat')
        f = Frame(self.main)
        f.pack(fill=BOTH, expand=1)
        table = TableCanvas(f, data=data, width=10, height=10)
        table.importCSV('../legacy/employees.csv')
        # print (table.model.columnNames)
        table.model.data[1]['a'] = 'XX'
        # table.model.setValueAt('TESTCHANGE',0,0)
        table.show()

        # add menubar at the top
        self.menubar = Menu(self.main, tearoff=False)
        self.main.config(menu=self.menubar)
        # create the file object)
        self.filemenu = Menu(self.menubar, tearoff=False)
        # New Employee
        # adds a command to the menu option, calling it exit
        self.filemenu.add_command(label="New Employee")
        # Logout
        self.filemenu.add_command(label="Logout", command=self.client_exit)
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

        buttons = Frame(self.main)

        self.add_button = Button(
            buttons,
            text="Add",
            command=lambda: table.showFilteringBar(),
            # font=('Arial', 14),
        )
        self.search_button = Button(
            buttons,
            text="Search",
            command=lambda: table.showFilteringBar(),
            # font=('Arial', 14),
        )
        self.delete_button = Button(
            buttons,
            text="Delete",
            # command=lambda: event_handlers['submit'](self.entry.get(), self.password_entry.get()),
            # font=('Arial', 14),
        )
        self.save_button = Button(
            buttons,
            text="Save",
            # command=lambda: event_handlers['submit'](self.entry.get(), self.password_entry.get()),
            # font=('Arial', 14),
        )

        self.add_button.pack(side=LEFT, anchor=W)
        Label(buttons, text='<user>').pack(side=LEFT, anchor=W)
        Label(buttons, text='Status').pack(side=LEFT, anchor=W)
        Frame(buttons, relief='flat', borderwidth=0).pack(fill=X, expand=1)
        self.save_button.pack(side=RIGHT, anchor=E)
        self.delete_button.pack(side=RIGHT, anchor=E)
        self.search_button.pack(side=RIGHT, anchor=E)

        buttons.pack(side=RIGHT, fill=X, expand=1)


    def client_exit(self):
        exit()
        return
        
def main(): 
    app=TestApp()
    app.mainloop()

if __name__ == "__main__":
    main()
