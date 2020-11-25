from lib.cli import import_csv
from lib.model.employee import Employee
from ui.control import Controller
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
            'file>logout': self.logout,
            'import>employees': self.import_employees,
            'import>receipts': self.import_receipts,
            'import>timesheets': self.import_timesheets
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
        self.view.table.redraw()

    def show(self):
        self.load()

        super().show()

    def new_employee(self):
        print('new employee!')
        self.view.new_employee()

    def import_employees(self):
        import_csv.import_employees(
            self.view.show_file_picker(
                title='Import Employees (CSV)',
                filetypes=('*.csv', '*.txt')
            ), from_cmd=False)
        self.refresh()

    def import_receipts(self):
        import_csv.import_receipts(
            self.view.show_file_picker(
                title='Import Receipts (CSV)',
                filetypes=('*.txt', '*.csv')
            ), from_cmd=False)
        self.refresh()

    def import_timesheets(self):
        import_csv.import_timesheets(
            self.view.show_file_picker(
                title='Import Time Sheets (CSV)',
                filetypes=('*.txt', '*.csv')
            ), from_cmd=False)
        self.refresh()

    def logout(self):
        exit()
