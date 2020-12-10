"""
Main View of the Application
"""
from tkinter import BOTH, Menu, LEFT, W, E, X, RIGHT
from tkinter.ttk import Frame, Button, Label

from lib.layer import security
from lib.model import employee
from lib.model.employee import Employee
from ui import store
from ui.widgets.table import EmpDatTableCanvas
from ui.window import TkinterWindow


class DatabaseWindow(TkinterWindow):
    """
    Shows employee table
    """

    def __init__(self, event_handlers):
        """
        Adds the table and it's options

        :param event_handlers: expects the following:
            'new_employee'
            'new_receipt'
            'new_timesheet'
            'run_payroll'
            'save'
            'delete'
            'file>logout'
            'import>employees'
            'import>receipts'
            'import>timesheets'
            'admin>review'
            'export>employees'
        """
        super().__init__(event_handlers)

        self.results = {}

        self.main = self.master
        self.main.geometry('1024x768')
        self.main.title('EmpDat')
        frame = Frame(self.main)
        frame.pack(fill=BOTH, expand=1)
        self.table = EmpDatTableCanvas(frame, col_modifiers={
            Employee.view_columns['id']: {  # ID
                'read_only': True
            },
            Employee.view_columns['role']: {  # Role
                'options': list(security.ROLES.keys())
            },
            Employee.view_columns['social_security_number']: {  # SSN
                'validator': 'ssn'
            },
            Employee.view_columns['start_date']: {  # Start Date
                'date': True,
                'validator': 'date',
            },
            Employee.view_columns['date_of_birth']: {  # DOB
                'date': True,
                'validator': 'date',
            },
            Employee.view_columns['sex']: {  # Sex
                'options': ['Male', 'Female', 'Other']
            },
            Employee.view_columns['state']: {  # State
                'validator': 'state_code'
            },
            Employee.view_columns['zipcode']: {  # Postal Code
                'validator': 'numeric'
            },
            Employee.view_columns['email']: {  # Email
                'validator': 'email'
            },
            Employee.view_columns['phone_number']: {  # Phone Number
                'validator': 'phone'
            },
            Employee.view_columns['emergency_contact_name']: {
                'validator': 'alpha'
            },
            Employee.view_columns['emergency_contact_phone']: {
                'validator': 'phone'
            },
            Employee.view_columns['classification']: {  # Classification
                'options': list(employee.classifications_dict.keys())
            },
            Employee.view_columns['payment_method']: {  # Payment Method
                'options': list(employee.pay_methods_dict.keys())
            },
            Employee.view_columns['salary']: {
                'validator': 'numeric'
            },
            Employee.view_columns['hourly_rate']: {
                'validator': 'numeric'
            },
            Employee.view_columns['commission_rate']: {
                'validator': 'numeric'
            },
            Employee.view_columns['bank_routing']: {
                'validator': 'bank_routing'
            },
            Employee.view_columns['bank_account']: {
                'validator': 'numeric'
            },
            Employee.view_columns['date_left']: {  # Date Left
                'date': True,
                'validator': 'date',
            },
        }, on_unsaved=self.on_table_unsaved,
                                       on_selected=lambda: self.set_delete_state('normal'),
                                       data=self.results, rowheight=50)
        self.table.show()

        if store.AUTHENTICATED_USER.role == 'Viewer':
            self.table.read_only = True

        self.create_menu()
        self.create_footer()

    def create_menu(self):
        """
        Creates top bar menu
        :return: None
        """

        # add menubar at the top
        self.menubar = Menu(self.main, tearoff=False)
        self.main.config(menu=self.menubar)
        # create the file object)
        self.filemenu = Menu(self.menubar, tearoff=False)
        # New Employee
        # adds a command to the menu option, calling it exit
        self.filemenu.add_command(label="New Employee",
                                  command=self.event_handlers['new_employee'])
        self.filemenu.add_command(label="New Receipt",
                                  command=self.event_handlers['new_receipt'])
        self.filemenu.add_command(label="New Timesheet",
                                  command=self.event_handlers['new_timesheet'])
        self.filemenu.add_separator()
        if store.AUTHENTICATED_USER.role == 'Admin' or store.AUTHENTICATED_USER.role == 'Accounting':
            self.filemenu.add_command(label="Run Payroll",
                                      command=self.event_handlers['run_payroll'])
        self.filemenu.add_command(label="Change My Password",
                                  command=self.event_handlers['change_my_password'])
        self.filemenu.add_separator()
        # Logout
        self.filemenu.add_command(label="Logout", command=self.event_handlers['file>logout'])
        # added "file" to our menu
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        # Reports Tab
        self.reports_menu = Menu(self.menubar, tearoff=False)
        # self.reports_menu.add_command(label="Paylog (CSV)",
        #                               command=None)
        self.reports_menu.add_command(label="Employee Directory (CSV)",
                                      command=self.event_handlers['export>employees'])
        self.reports_menu.add_command(label="Employee Directory (PDF)",
                                      command=self.event_handlers['export>pdf_employees'])
        self.menubar.add_cascade(label="Reports", menu=self.reports_menu)
        # Import tab
        self.import_menu = Menu(self.menubar, tearoff=False)
        self.import_menu.add_command(label="Employees (Legacy)",
                                     command=self.event_handlers['import>employees'])
        self.import_menu.add_command(label="Receipts",
                                     command=self.event_handlers['import>receipts'])
        self.import_menu.add_command(label="Timesheets",
                                     command=self.event_handlers['import>timesheets'])
        self.menubar.add_cascade(label="Import", menu=self.import_menu)
        # Admin tab
        if store.AUTHENTICATED_USER.role == 'Admin':
            self.admin_menu = Menu(self.menubar, tearoff=False)
            self.admin_menu.add_command(label="Review Change Requests",
                                        command=self.event_handlers['admin>review'])
            self.admin_menu.add_command(label="Change Passwords",
                                        command=self.event_handlers['admin>change_password'])
            self.menubar.add_cascade(label="Admin", menu=self.admin_menu)

    def create_footer(self):
        """
        Creates utility footer
        :return:
        """
        buttons = Frame(self.main)

        self.new_button = Button(
            buttons,
            text="New",
            command=self.event_handlers['new_employee'],
        )
        self.search_button = Button(
            buttons,
            text="Search",
            command=self.table.showFilteringBar,
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
        Label(buttons,
              text=f"({store.AUTHENTICATED_USER.first_name} "
              f"{store.AUTHENTICATED_USER.last_name})") \
            .pack(side=LEFT, anchor=W)

        self.status = Label(buttons, text='')
        self.status.pack(side=LEFT, anchor=W)

        Frame(buttons, relief='flat', borderwidth=0).pack(fill=X, expand=1)

        self.save_button.pack(side=RIGHT, anchor=E)
        self.delete_button.pack(side=RIGHT, anchor=E)
        self.search_button.pack(side=RIGHT, anchor=E)

        buttons.pack(side=RIGHT, fill=X, expand=1)

    def on_table_unsaved(self, is_unchanged: bool, row=None, col=None):
        self.set_save_state('normal' if not is_unchanged else 'disabled')
        if row and col:
            if not is_unchanged:
                self.table.model.setColorAt(row, col, 'gold')
            else:
                self.table.model.setColorAt(row, col, 'white')
            self.table.redrawTable()

    def on_before_save(self):
        for row_name in self.table.unsaved:
            row_index = self.table.model.getRecordIndex(row_name)
            for col in range(0,self.table.model.getColumnCount()):
                self.table.model.setColorAt(row_index, col, 'white')
                self.table.redrawCell(row_index, col)

    def highlight_invalid_rows(self, ids):
        for row_id in ids:
            row_index = self.table.model.getRecordIndex(row_id)
            for col in range(0, self.table.model.getColumnCount()):
                self.table.model.setColorAt(row_index, col, 'coral')
                self.table.redrawCell(row_index, col)

    def highlight_invalid_cell(self, row_id, col_name):
        row_index = self.table.model.getRecordIndex(row_id)
        col_index = self.table.model.getColumnIndex(col_name)

        self.table.model.setColorAt(row_index, col_index, 'coral')
        self.table.redrawCell(row_index, col_index)

    def set_save_state(self, state):
        """
        Sets state of the save button
        :param state: tkinter button state
        :return: None
        """
        self.save_button['state'] = state

    def set_delete_state(self, state):
        """
        Sets state of the delete button
        :param state: tkinter button state
        :return: None
        """
        self.delete_button['state'] = state

    def new_employee(self, new_id, view_model):
        """
        Handle employee creation
        :return:
        """
        record_id = f"NEW{new_id}"
        view_model['ID'] = record_id
        self.add_to_result(record_id, view_model)
        self.table.movetoSelectedRow(recname=record_id)

    def add_to_result(self, record_id, to_add: dict):
        """
        Add a row to table
        :param record_id: record id
        :param to_add: view model to add
        :return: None
        """
        self.table.addRow(record_id, **to_add)

    def destroy_results(self):
        """
        Destroy all rows
        :return: None
        """
        keys = list(self.table.model.data.keys())
        for key in keys:
            self.table.model.deleteRow(key=key)

    def set_status(self, text: str):
        """
        Sets status text at the footer
        :param text: message to display
        :return: None
        """
        self.status.configure(text=text)


if __name__ == "__main__":
    db_page = DatabaseWindow({})
    db_page.mainloop()

# mainloop method will loop forever, waiting for events from the user,
# until the user exits the program -
# either by closing the window, or by terminating the program with a
# keyboard interrupt in the console.


# Time spent:
# 10/20: 2.5 hours
# 10/26: 0.25 hours
