"""
Change Requests view
"""

import json
from tkinter import BOTH, RIGHT, E, X
from tkinter.ttk import Frame, Button

from lib.model import find_model_by_name
from lib.model.change_request import ChangeRequest
from ui.widgets.table import EmpDatTableCanvas
from ui.window import TkinterWindow


def _render_row_id(raw: str) -> str:
    """
    Hook to prettify the Employee who initated the change
    :param raw: json given in field by the controller
    :return: pretty row_id (with name)
    """
    loaded = json.loads(raw)
    table_name = loaded[0]
    row_id = loaded[1]

    if row_id:
        try:
            return find_model_by_name(table_name).read(row_id).get_name()
        except AttributeError:
            pass
    return 'NEW'


class ChangeRequestsWindow(TkinterWindow):
    """
    Change Requests view
    """

    def __init__(self, event_handlers):
        """
        Adds the table and the bottom buttons
        :param event_handlers: expects 'approve' and 'reject'
        """
        super().__init__(event_handlers)

        self.results = {}

        self.master.geometry('1024x768')
        self.master.title('Change Requests')
        frame = Frame(self.master)
        frame.pack(fill=BOTH, expand=1)
        self.table = EmpDatTableCanvas(frame,
                                       col_modifiers={
                                           'ID affected': {
                                               'render_as': lambda x: _render_row_id(x)  # pylint: disable=unnecessary-lambda
                                           },
                                           'Changes': {
                                               'render_as': lambda x:
                                               ChangeRequest.prettify_changes(*json.loads(x))
                                           }
                                       },
                                       on_selected=lambda: self.set_bottom_state('normal'),
                                       data=self.results, rowheight=150)
        self.table.show()
        self.table.read_only = True

        self.create_bottom()

    def create_bottom(self):
        """
        Approve and reject buttons
        :return: None
        """
        buttons = Frame(self.master)

        self.reject_button = Button(
            buttons,
            text="Reject",
            command=self.event_handlers['reject'],
            state='disabled'
        )
        self.approve_button = Button(
            buttons,
            text="Approve",
            command=self.event_handlers['approve'],
            state='disabled'
        )

        self.approve_button.pack(side=RIGHT, anchor=E)
        self.reject_button.pack(side=RIGHT, anchor=E)

        buttons.pack(side=RIGHT, fill=X, expand=1)

    def set_bottom_state(self, state):
        """
        Utility for disabling/enabling the bottom buttons
        :param state: Tkinter button state str
        :return: None
        """
        self.approve_button['state'] = state
        self.reject_button['state'] = state

    def add_to_result(self, record_id, to_add: dict):
        """
        Adds a view model to the table
        :param record_id: record ID
        :param to_add: view model to add
        :return: None
        """
        to_add['ID affected'] = json.dumps((to_add['Data Type'], to_add['ID affected']))
        to_add['Changes'] = json.dumps((to_add['Changes'], to_add['Data Type']))
        self.table.addRow(record_id, **to_add)

    def destroy_results(self):
        """
        Destroy all rows
        :return: None
        """
        keys = list(self.table.model.data.keys())
        for key in keys:
            self.table.model.deleteRow(key=key)
