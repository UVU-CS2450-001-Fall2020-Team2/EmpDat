"""
Main Controller of application
"""

import datetime
import sys

from lib import exporter
from lib.cli import import_csv
from lib.cli.payroll import run_payroll
from lib.layer.security import ChangeRequestException, SecurityException
from lib.model.employee import Employee
from lib.model.receipt import Receipt
from lib.model.timesheet import TimeSheet
from lib.repository.validator import is_valid_against, ValidationException
from lib.utils import sha_hash
from ui import store
from ui.control import Controller
from ui.control.change_requests import ChangeRequestsController
from ui.window.database import DatabaseWindow
from ui.window.dialogs.about_empdat import AboutEmpDatDialog
from ui.window.dialogs.add_receipt import AddReceiptDialog
from ui.window.dialogs.add_timesheet import AddTimesheetDialog
from ui.window.dialogs.my_password import MyPasswordDialog
from ui.window.dialogs.others_password import PasswordDialog


def _open_change_requests():
    """
    Shows change requests window
    :return: None
    """
    ChangeRequestsController().show()


def _on_password_save(view, dialog, employee_id, old_pass: str,  # pylint: disable=too-many-arguments
                      password: str, password_confirm: str, require_old=True):
    employee = Employee.read(employee_id)

    if require_old and sha_hash(old_pass) != employee.password:
        view.show_error('Error', 'Old password does not match!')
        return

    if password != password_confirm:
        view.show_error('Error', 'New Passwords do not match!')
        return

    if not is_valid_against('password', password):
        view.show_error('Error', 'Passwords must have at least 9 characters (with at least '
                                 '1 number, 1 special character, and upper and lowercase '
                                 'characters)!')
        return

    Employee.read(employee_id).update_password(password)

    view.set_status('Changing password successful!')
    view.show_info('Info', 'Changing password successful!')
    dialog.destroy()


class DatabaseController(Controller):
    """
    Controller for the employee table view
    """

    def __init__(self):
        """
        Uses DatabaseWindow
        """
        super().__init__(DatabaseWindow({
            'new_employee': self.new_employee,
            'new_receipt': self.new_receipt,
            'new_timesheet': self.new_timesheet,
            'run_payroll': self.run_payroll,
            'change_my_password': self.change_my_password,
            'save': self.save,
            'delete': self.delete,
            'refresh': self.refresh,
            'file>logout': self.logout,
            'import>employees': self.import_employees,
            'import>receipts': self.import_receipts,
            'import>timesheets': self.import_timesheets,
            'admin>review': _open_change_requests,
            'admin>change_password': self.change_password,
            'export>employees': self.export_to_csv,
            'export>pdf_employees': self.export_to_pdf,
            'help>about_empdat': self.about_empdat,
        }))

        self.new_id = 0

    def load(self):
        """
        Loads all employees and displays them on the table
        :return: None
        """
        employees = Employee.read_all()
        i = 0
        for employee in employees:
            i += 1
            self.view.add_to_result(employee.id,
                                    employee.to_view_model(security_layer=store.SECURITY_LAYER))

        self.view.table.autoResizeColumns()

    def refresh(self):
        """
        Wipes and reloads the table
        :return: None
        """
        self.view.destroy_results()
        self.load()
        self.view.table.unsaved = set()
        self.view.table.redraw()

    def show(self):
        """
        Overrides show to load data first
        :return: None
        """
        self.load()

        super().show()

    def run_payroll(self):
        """
        Runs the payroll process, asks where to save it
        :return: None
        """
        filepath = self.view.show_save_picker(
            title='Save Payroll',
            filetypes=[('Text File', '*.txt')]
        )

        if not filepath:
            self.view.set_status('Payroll cancelled')
            return

        run_payroll(filepath)
        self.view.show_info('Success', f'Payroll was processed and was written to: {filepath}!')
        self.view.set_status('Payroll was processed successfully!')

    def save(self):
        """
        When Save is pressed, the change is either performed, or a change request is submitted
        :return: None
        """
        self.view.on_before_save()
        change_request_submitted = False
        for employee_id in self.view.table.unsaved:
            view_model = self.view.table.model.data[employee_id]

            is_new = False
            if isinstance(employee_id, str) and "NEW" in employee_id:
                view_model[Employee.view_columns['id']] = None
                is_new = True

            try:
                employee = Employee.from_view_model(view_model)
                if is_new:
                    Employee.create(employee)
                else:
                    Employee.update(employee)
            except ChangeRequestException:
                change_request_submitted = True
            except SecurityException as error:
                self.view.highlight_invalid_rows([employee_id])
                self.view.show_error('Error', f'Access Denied\n{error}')
                return
            except ValidationException as error:
                self.view.highlight_invalid_cell(employee_id,
                                                 Employee.view_columns[error.database_field])
                self.view.show_error('Error', f'Invalid data: {error}')
                self.view.set_status(f'Invalid data: {error}')
                return

        if change_request_submitted:
            self.view.show_info('Success', 'Request to Change Submitted!')
            self.view.set_status(f'Request to Change {len(self.view.table.unsaved)} '
                                 f'employees Submitted!')
        else:
            self.view.set_status(f'Saved {len(self.view.table.unsaved)} employees successfully!')
            self.view.master.bell()
        self.refresh()

    def delete(self):
        """
        When Delete is pressed, the change is either performed, or a change request is submitted
        :return: None
        """
        if self.view.show_confirm(title='Confirm Employee Deletion',
                                  message='Are you sure you want to delete the employee(s)?'):
            ids = self.view.table.get_selectedRecordNames()
            for employee_id in ids:
                try:
                    Employee.destroy(employee_id)
                except SecurityException:
                    self.view.show_error('Access Denied', 'Insufficient permission to delete '
                                                          'selected employees')
                    self.refresh()
                    break
            self.view.show_info('Deletion Successful', 'The selected employee(s) '
                                                       'were deleted successfully!')
            self.refresh()

    def new_employee(self):
        """
        When New is pressed.
        :return: None
        """
        self.view.new_employee(self.new_id, Employee.new_empty().to_view_model())
        self.new_id += 1

    def change_my_password(self):
        """
        Shows the change my password dialog and saves it
        :return: None
        """

        def on_save(dialog, old_pass: str, password: str, password_confirm: str):
            _on_password_save(self.view, dialog, store.SECURITY_LAYER.user.id,
                              old_pass, password, password_confirm)

        MyPasswordDialog({
            'save': on_save
        })

    def change_password(self):
        """
        Shows the change others' passwords dialog and saves it
        :return: None
        """

        def on_save(dialog, employee_id, password: str, password_confirm: str):
            _on_password_save(self.view, dialog, employee_id, None,
                              password, password_confirm, require_old=False)

        PasswordDialog({
            'save': on_save
        }, Employee.read_all())

    def import_employees(self):
        """
        Uses import csv library from CLI
        :return: None
        """
        filepath = self.view.show_file_picker(
            title='Import Employees (CSV)',
            filetypes=(('CSV File', '*.csv'), ('Text File', '*.txt'))
        )

        if not filepath:
            self.view.set_status('Importing employees cancelled')
            return

        import_csv.import_employees(filepath, from_cmd=False)
        self.view.set_status('Importing employees successful!')
        self.refresh()

    def import_receipts(self):
        """
        Uses import csv library from CLI
        :return: None
        """
        filepath = self.view.show_file_picker(
            title='Import Receipts',
            filetypes=(('Text File', '*.txt'), ('CSV File', '*.csv'))
        )

        if not filepath:
            self.view.set_status('Importing receipts cancelled')
            return

        import_csv.import_receipts(filepath, from_cmd=False)
        self.view.set_status('Importing receipts successful!')
        self.refresh()

    def import_timesheets(self):
        """
        Uses import csv library from CLI
        :return: None
        """
        filepath = self.view.show_file_picker(
            title='Import Time Sheets',
            filetypes=(('Text File', '*.txt'), ('CSV File', '*.csv'))
        )

        if not filepath:
            self.view.set_status('Importing time sheets cancelled')
            return

        import_csv.import_timesheets(filepath, from_cmd=False)
        self.view.set_status('Importing time sheets successful!')
        self.refresh()

    def new_receipt(self):
        """
        Shows the add receipt dialog and saves it
        :return: None
        """

        def on_save(dialog, employee_id: int, amount: float):
            try:
                amount = float(amount)
            except ValueError:
                self.view.show_error('Error', 'Invalid amount given!')
                return

            if Employee.read(employee_id):
                receipt = Receipt({
                    'user_id': employee_id,
                    'amount': amount
                })
                try:
                    Receipt.create(receipt)
                    self.view.show_info('Info', 'Receipt created successfully!')
                except SecurityException as error:
                    self.view.show_error('Error', f'Unable to create receipt: {error}')
                    return
                except ChangeRequestException:
                    self.view.show_info('Info', 'A change request has been created '
                                                'and will be reviewed.')

            self.view.set_status('Receipt creation successful!')
            dialog.destroy()

        AddReceiptDialog({
            'save': on_save
        }, Employee.read_all())

    def new_timesheet(self):
        """
        Shows the add timesheet dialog and saves it
        :return: None
        """

        def on_save(dialog, employee_id: int, date: datetime.date,  # pylint: disable=too-many-arguments
                    hour_in, min_in, hour_out, min_out):
            try:
                hour_in = int(hour_in)
                min_in = int(min_in)
                hour_out = int(hour_out)
                min_out = int(min_out)
            except ValueError:
                self.view.show_error('Error', 'Invalid dates given!')
                return

            time_begin = datetime.datetime.strptime(f"{hour_in} {min_in}", "%H %M").time()
            time_end = datetime.datetime.strptime(f"{hour_out} {min_out}", "%H %M").time()
            datetime_begin = datetime.datetime.combine(date, time_begin)
            datetime_end = datetime.datetime.combine(date, time_end)

            if Employee.read(employee_id):
                timesheet = TimeSheet({
                    'user_id': employee_id,
                    'datetime_begin': datetime_begin,
                    'datetime_end': datetime_end,
                })
                try:
                    TimeSheet.create(timesheet)
                    self.view.show_info('Success', 'Timesheet created successfully!')
                except SecurityException:
                    self.view.show_error('Error', 'Access Denied')
                    return
                except ChangeRequestException:
                    self.view.show_info('Info', 'A change request has been created '
                                                'and will be reviewed.')
            self.view.set_status('Timesheet creation successful!')
            dialog.destroy()

        AddTimesheetDialog({
            'save': on_save
        }, Employee.read_all())

    def export_to_csv(self):
        """
        Exports the table to a CSV
        :return: None
        """
        self.view.table.exportTable()

    def export_to_pdf(self):
        """
        Exports the table to a PDF
        :return: None
        """
        filepath = self.view.show_save_picker(
            title='Export Employee Directory (PDF)',
            filetypes=[('PDF Document', '*.pdf')]
        )

        if not filepath:
            self.view.set_status('Export cancelled')
            return

        try:
            if not exporter.html_to_pdf(exporter.table_to_html(self.view.table.model), filepath):
                self.view.show_error('Export Failed!', 'An error occurred while creating the PDF!')
                self.view.set_status('Export Failed!')
            else:
                self.view.show_info('Export Success!', 'The PDF was created successfully!')
                self.view.set_status('Export Success!')
        except IOError as error:
            self.view.show_error('Export Failed!', f'An error occurred '
            f'while creating the PDF! {error}')
            self.view.set_status('Export Failed!')

    def about_empdat(self):  # pylint: disable=no-self-use
        """
        Shows the About EmpDat Dialog
        :return: None
        """
        AboutEmpDatDialog()

    def logout(self):  # pylint: disable=no-self-use
        """
        Logout hook. Currently unused. Exits the app
        :return: None
        """
        sys.exit()
