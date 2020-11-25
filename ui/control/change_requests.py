from lib.model.change_request import ChangeRequest
from ui.control import Controller
from ui.window.change_requests import ChangeRequestsWindow


class ChangeRequestsController(Controller):

    def __init__(self):
        super().__init__(ChangeRequestsWindow({
            # 'submit': self.login
        }))

    def load(self):
        change_requests = ChangeRequest.read_all()
        i = 0
        for request in change_requests:
            i += 1
            self.view.add_to_result(request.id, request.to_view_model())

        # if i == 0:
        #     self.view.add_to_result(-1, {'No Employees found!': 'Click Import > Employees to begin'})

        self.view.table.autoResizeColumns()

    def refresh(self):
        self.load()
        self.view.table.redraw()

    def show(self):
        self.load()

        super().show()