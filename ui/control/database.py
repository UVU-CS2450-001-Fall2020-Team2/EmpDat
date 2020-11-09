from lib.model.employee import Employee
from ui.control import Controller
from ui.control.employee import EmployeeController
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
            'edit_employee': self.edit_employee
        }))

    def show(self):
        self.view.setup_grid()

        employees = Employee.read_all()
        for employee in employees:
            self.view.add_to_result({
                "id": employee.id,
                "name": f"{employee.last_name}, {employee.first_name}",
                "address": f"{employee.address_line1} {employee.address_line2}",
                "city": employee.city,
                "state": employee.state,
                "zip": employee.zipcode,
                "classification": "hi",
                "pay_method": employee.id
            })

        super().show()

    def edit_employee(self, emp_id):
        EmployeeController(emp_id).show()