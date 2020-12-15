"""
Controller for Change Requests admin window
"""

from lib.model.change_request import ChangeRequest
from ui import store
from ui.control import Controller
from ui.window.change_requests import ChangeRequestsWindow


class ChangeRequestsController(Controller):
    """
    Controller for Change Requests admin window
    """

    def __init__(self):
        """
        Supplies the approve and reject methods to the view
        """
        super().__init__(ChangeRequestsWindow({
            'approve': self.approve,
            'reject': self.reject,
        }))

    def load(self):
        """
        Loads all change requests and has the view display them
        :return: None
        """
        change_requests = ChangeRequest.read_by(filters={
            'approved_at': None
        })
        i = 0
        for request in change_requests:
            i += 1
            self.view.add_to_result(request.id, request.to_view_model())

        self.view.table.autoResizeColumns()

    def refresh(self):
        """
        Wipes and refreshes change requests view
        :return: None
        """
        self.view.destroy_results()
        self.load()
        self.view.table.redraw()

    def show(self):
        self.load()

        super().show()

    def approve(self):
        """
        On approve change
        :return: None
        """
        ids = self.view.table.get_selectedRecordNames()
        for request_id in ids:
            request = ChangeRequest.read(request_id)
            request.apply_to_db(store.SECURITY_LAYER.user)
        self.view.show_info('Approvals Successful', 'Changes applied successfully!')
        self.refresh()

    def reject(self):
        """
        On reject change
        :return: None
        """
        ids = self.view.table.get_selectedRecordNames()
        for request_id in ids:
            ChangeRequest.destroy(request_id)
        self.view.show_info('Approvals Rejections', 'Changes rejected successfully!')
        self.refresh()
