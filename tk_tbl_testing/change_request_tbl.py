from tkintertable import TableCanvas, TableModel
from tkinter import *
import random
from collections import OrderedDict
from changeRequest import changeRequest

from tkintertable.Testing import sampledata
#data=sampledata()
#print(data)

class TestApp(Frame):
    """Basic test frame for the table"""
    

    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('800x500+200+100')
        self.main.title('Test')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        obj = changeRequest(); 
        self.data = {
        'change1': {'ID': obj.id,'Created': obj.created_at,'Updated': obj.updated_at,
        'Old Value': obj.field_name, 'New Value': obj.field_new_value,
        'Reason': obj.reason, 'Approved?': obj.approved_at }}
        table = TableCanvas(f, data=self.data)
        #table.importCSV('test.csv')
        print (table.model.columnNames)
        #table.model.data[1]['a'] = 'XX'
        #table.model.setValueAt('YY',0,2)
        table.show()
        return

app=TestApp()
app.mainloop()