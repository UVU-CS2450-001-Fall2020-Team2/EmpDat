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
        }))

    def show(self):
        employees = Employee.read_all()
        for employee in employees:
            self.view.add_to_result(employee.id, {
                "ID": employee.id,
                "Name": f"{employee.last_name}, {employee.first_name}",
                "Address": f"{employee.address_line1} {employee.address_line2}",
                "City": employee.city,
                "State": employee.state,
                "Postal": employee.zipcode,
                "Class": "hi",
                "Payment Method": employee.id
            })

        self.view.table.autoResizeColumns()

        super().show()