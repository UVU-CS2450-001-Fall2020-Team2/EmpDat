import json
from tkinter import *

from lib.model import find_model_by_name
from lib.model.change_request import ChangeRequest
from ui.widgets.table import EmpDatTableCanvas
from ui.window import TkinterWindow


class ChangeRequestsWindow(TkinterWindow):

    def __init__(self, event_handlers):
        super().__init__(event_handlers)

        self.results = {}

        self.master.geometry('1024x768')
        self.master.title('Change Requests')
        f = Frame(self.master)
        f.pack(fill=BOTH, expand=1)
        self.table = EmpDatTableCanvas(f, col_modifiers={
            2: {
                'render_as': lambda x: self.render_row_id(x)
            },
            3: {
                'render_as': lambda x: ChangeRequest.prettify_changes(*json.loads(x))
            }
        }, data=self.results, rowheight=50)
        self.table.show()
        self.table.read_only = True

    def add_to_result(self, id, to_add: dict):
        to_add['ID affected'] = json.dumps((to_add['Data Type'], to_add['ID affected']))
        to_add['Changes'] = json.dumps((to_add['Changes'], to_add['Data Type']))
        self.table.addRow(id, **to_add)

    def render_row_id(self, raw):
        loaded = json.loads(raw)
        table_name = loaded[0]
        row_id = loaded[1]
        return find_model_by_name(table_name).read(row_id).get_name()

