from lib.cli import import_csv
from lib.layer.security import ChangeRequestException, SecurityException
from lib.model.employee import Employee
from ui.control import Controller
from ui.control.change_requests import ChangeRequestsController
from ui.window.database import DatabaseWindow


# self.columns = {
#             "id": Label(database, text="ID"),
#             "name": Label(database, text="Name"),
#             "address": Label(database, text="Address"),
#             "city": Label(database, text="City"),
#             "state": Label(database, text="State"),
#             "zip": Label(database, text="Zip"),
#             "classification": Label(database, text="Classification"),
#             "pay_method": Label(database, text="Pay Method"),
#         }

class DatabaseController(Controller):

    def __init__(self):
        super().__init__(DatabaseWindow({
            'new_employee': self.new_employee,
            'save': self.save,
            'delete': self.delete,
            'file>logout': self.logout,
            'import>employees': self.import_employees,
            'import>receipts': self.import_receipts,
            'import>timesheets': self.import_timesheets,
            'add>receipts': self.add_receipts,
            'add>timesheets': self.add_timesheets,
            'admin>review': self.open_change_requests,
        }))

    def load(self):
        employees = Employee.read_all()
        i = 0
        for employee in employees:
            i += 1
            self.view.add_to_result(employee.id, employee.to_view_model())
        #
        # if i == 0:
        #     self.view.add_to_result(-1, {'No Employees found!': 'Click Import > Employees to begin'})

        self.view.table.autoResizeColumns()

    def refresh(self):
        self.view.destroy_results()
        self.load()
        self.view.table.unsaved = []
        self.view.table.redraw()

    def show(self):
        self.load()

        super().show()

    def save(self):
        change_request_submitted = False
        for employee_id in self.view.table.unsaved:
            view_model = self.view.table.model.data[employee_id]
            employee = Employee.from_view_model(view_model)
            try:
                Employee.update(employee)
            except ChangeRequestException:
                change_request_submitted = True

        if change_request_submitted:
            self.view.show_info('Request to Change Submitted!')
            self.view.set_status(f'Request to Change {len(self.view.table.unsaved)} employees Submitted!')
        else:
            self.view.set_status(f'Saved {len(self.view.table.unsaved)} employees successfully!')
        self.refresh()

    def delete(self):
        ids = self.view.table.get_selectedRecordNames()
        for employee_id in ids:
            try:
                Employee.destroy(employee_id)
            except SecurityException:
                self.view.show_error('Access Denied', 'Insufficient permission to delete selected employees')
                self.refresh()
                break
        self.view.show_info('Deletion Successful', 'The selected employee(s) were deleted successfully!')
        self.refresh()

    def new_employee(self):
        print('new employee!')
        self.view.new_employee()

    def import_employees(self):
        import_csv.import_employees(
            self.view.show_file_picker(
                title='Import Employees (CSV)',
                filetypes=('*.csv', '*.txt')
            ), from_cmd=False)
        self.view.set_status(f'Importing employees successful!')
        self.refresh()

    def import_receipts(self):
        import_csv.import_receipts(
            self.view.show_file_picker(
                title='Import Receipts (CSV)',
                filetypes=('*.txt', '*.csv')
            ), from_cmd=False)
        self.view.set_status(f'Importing receipts successful!')
        self.refresh()

    def import_timesheets(self):
        import_csv.import_timesheets(
            self.view.show_file_picker(
                title='Import Time Sheets (CSV)',
                filetypes=('*.txt', '*.csv')
            ), from_cmd=False)
        self.view.set_status(f'Importing time sheets successful!')
        self.refresh()

    def add_receipts(self):
        self.main = Toplevel(self.main)
        self.main.geometry = ('200 x 200')
        self.emp_label = tkinter.Label(self.main,
                            text = "Which employee is the receipt for?")
        self.emp_label.grid(column=0, row=0)
        tkvar = StringVar(self.main)

        # Dictionary with options
        choices = {'Joe','John','Suzie','Phil','Allison'}
        tkvar.set('Joe') # set the default option
        popupMenu = OptionMenu(self.main, tkvar, *choices)
        popupMenu.grid(column= 1, row = 0)

        self.amount_lbl = tkinter.Label(self.main,
                            text = "How much did they pay?")
        self.amount_lbl.grid(column = 0, row = 1)
        self.amount = tkinter.Entry(self.main)
        self.amount.grid(column = 1, row = 1)
        self.save_btn = Button(self.main, text = "Save", command= None) 
        #need to change commands
        self.save_btn.grid(column = 0, row = 2)
        self.cancel_btn = Button(self.main, text = "Cancel", command= None) 
        #need to change commands
        self.cancel_btn.grid(column = 1, row = 2)

    def add_timesheets(self):
        self.main = Toplevel(self.main)
        self.main.geometry = ('200 x 200')
        self.frame1 = Frame(self.main)
        self.frame1.pack(side = TOP)
        self.emp_label = tkinter.Label(self.frame1,
                            text = "Which employee is the timesheet for?")
        self.emp_label.pack(side = LEFT)
        tkvar = StringVar(self.main)
        # Dictionary with options
        choices = { 'Joe','John','Suzie','Phil','Allison'}
        tkvar.set('Joe') # set the default option
        popupMenu = OptionMenu(self.frame1, tkvar, *choices)
        popupMenu.pack(side= LEFT)
        self.frame2 = Frame(self.main)
        self.frame2.pack(side = TOP)
        self.date_lbl = tkinter.Label(self.frame2, text='Choose date: ')
        self.date_lbl.pack(side = LEFT)
        self.cal = DateEntry(self.frame2, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
        self.cal.pack(side = LEFT)
        self.frame3 = Frame(self.main)
        self.frame3.pack(side = TOP)
        self.clock_in = tkinter.Label(self.frame3, text = "Clock in: ")
        # self.hour_1 = tkinter.Entry(self.frame3, width=2,validatecommand=self.vcmd)
        self.hour_1 = tkinter.Entry(self.frame3, width=2)
        self.colon_1 = tkinter.Label(self.frame3, text=':')
        self.min_1 = tkinter.Entry(self.frame3, width=2)
        # self.min_1 = tkinter.Entry(self.frame3, width=2, validatecommand=self.vcmd)
        #self.vcmd = (self.main.register(self.do_validation), '%P')
        #def do_validation(new_value):
        #    return new_value == "" or new_value.isnumeric()
        self.clock_in.pack(side = LEFT)
        self.hour_1.pack(side = LEFT)
        self.colon_1.pack(side = LEFT)
        self.min_1.pack(side = LEFT)
        self.frame4 = Frame(self.main)
        self.frame4.pack(side = TOP)
        self.clock_out = tkinter.Label(self.frame4, text = "Clock out: ")
        self.hour_2 = tkinter.Entry(self.frame4, width=2)
        self.colon_2 = tkinter.Label(self.frame4, text=':')
        self.min_2 = tkinter.Entry(self.frame4, width=2)
        self.clock_out.pack(side = LEFT)
        self.hour_2.pack(side = LEFT)
        self.colon_2.pack(side = LEFT)
        self.min_2.pack(side = LEFT)
        self.frame5 = Frame(self.main)
        self.frame5.pack(side = TOP)
        self.save_btn = Button(self.frame5, text = "Save", command= None) 
        self.save_btn.pack(side = LEFT)
        self.cancel_btn = Button(self.frame5, text = "Cancel", command= None) 
        self.cancel_btn.pack(side = LEFT)
        
        

    def open_change_requests(self):
        ChangeRequestsController().show()

    def logout(self):
        exit()
