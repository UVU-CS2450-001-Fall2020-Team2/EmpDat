from tkintertable import TableCanvas, TableModel
from tkinter import *
import random
from collections import OrderedDict

data = {'rec1': {'firstName': 'John', 'lastName': 'Doe', 'classification': 'salary'},
       'rec2': {'firstName': 'Suzie', 'lastName': 'Johnson', 'classification': 'salary'},
       'rec3': {'firstName': 'Phil', 'lastName': 'Harris', 'classification': 'salary'}
       }

# from tkintertable.Testing import sampledata
# data=sampledata()
#print(data)

class TestApp(Frame):
    """Basic test frame for the table"""

    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('800x500+200+100')
        self.main.title('EmpDat')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        table = TableCanvas(f, data=data)
        table.importCSV('/Users/tolsen/tmp/employees.csv')
        #print (table.model.columnNames)
        table.model.data[1]['a'] = 'XX'
        #table.model.setValueAt('TESTCHANGE',0,0)
        table.show()

        #add menubar at the top
        self.menubar = Menu(self.main)
        self.main.config(menu=self.menubar)
        # create the file object)
        self.filemenu = Menu(self.menubar)
        #New Employee
        # adds a command to the menu option, calling it exit
        self.filemenu.add_command(label="New Employee")
        #Logout
        self.filemenu.add_command(label="Logout",command=self.client_exit)
        #added "file" to our menu
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        #Reports Tab
        self.reports_menu = Menu(self.menubar)
        self.reports_menu.add_command(label="Paylog")
        self.reports_menu.add_command(label = "Employee Directory")
        self.menubar.add_cascade(label = "Reports", menu = self.reports_menu)
        #Import tab
        self.import_menu = Menu(self.menubar)
        self.import_menu.add_command(label="Employee", command = None)
        self.import_menu.add_command(label = "Receipt", command = None)
        self.import_menu.add_command(label = "Timesheet", command = None)
        self.menubar.add_cascade(label = "Import", menu = self.import_menu)
    
    def client_exit(self):
        exit()
        return

app=TestApp()
app.mainloop()
