from ui.control import Controller
from ui.window.new_employee import NewEmployeeWindow, EditEmployeeWindow


class EmployeeController(Controller):

    def __init__(self, employee_id=None):
        if not employee_id:
            super().__init__(NewEmployeeWindow({
                # 'submit': self.login
            }))
        else:
            super().__init__(EditEmployeeWindow({
                # 'submit': self.login
            }))

    def show(self):
        self.view.setup_grid()
        super().show()
