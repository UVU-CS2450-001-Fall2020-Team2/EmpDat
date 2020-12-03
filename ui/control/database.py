from lib.cli import import_csv
from lib.layer.security import ChangeRequestException, SecurityException
from lib.model.employee import Employee
from ui.control import Controller
from ui.control.change_requests import ChangeRequestsController
from ui.window.database import DatabaseWindow
from ui.window.dialogs.add_receipt import AddReceiptDialog
from ui.window.dialogs.add_timesheet import AddTimesheetDialog


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
            'export>employees': self.export_to_csv,
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

        def on_save(dialog):
            print('on save!')
            dialog.destroy()

        AddReceiptDialog({
            'save': on_save
        }, Employee.read_all())

    def add_timesheets(self):
        def on_save(dialog):
            print('on save!')

        AddTimesheetDialog({
            'save': on_save
        }, Employee.read_all())

    def open_change_requests(self):
        ChangeRequestsController().show()

    def export_to_csv(self):
        self.view.table.exportTable()

    def logout(self):
        exit()
