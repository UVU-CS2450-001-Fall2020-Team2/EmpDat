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
            'file>logout': self.logout
        }))

    def show(self):
        employees = Employee.read_all()
        for employee in employees:
            self.view.add_to_result(employee.id, employee.to_view_model())

        self.view.table.autoResizeColumns()

        super().show()

    def new_employee(self):
        print('new employee!')
        self.view.new_employee()

    def logout(self):
        exit()
