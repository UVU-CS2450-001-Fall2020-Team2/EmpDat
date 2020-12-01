from lib.model.change_request import ChangeRequest
from ui import store
from ui.control import Controller
from ui.window.change_requests import ChangeRequestsWindow


class ChangeRequestsController(Controller):

    def __init__(self):
        super().__init__(ChangeRequestsWindow({
            'approve': self.approve,
            'reject': self.reject,
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

    def approve(self):
        ids = self.view.table.get_selectedRecordNames()
        for request_id in ids:
            request = ChangeRequest.read(request_id)
            request.apply_to_db(store.AUTHENTICATED_USER)
        self.view.show_info('Approvals Successful', 'Changes applied successfully!')
        self.refresh()

    def reject(self):
        ids = self.view.table.get_selectedRecordNames()
        for request_id in ids:
            ChangeRequest.destroy(request_id)
        self.view.show_info('Approvals Rejections', 'Changes rejected successfully!')
        self.refresh()
