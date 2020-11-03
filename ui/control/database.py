from ui.control import Controller
from ui.store import TK_ROOT
from ui.window.database import DatabaseWindow


class DatabaseController(Controller):

    def __init__(self):
        super().__init__(DatabaseWindow(TK_ROOT, {
            # 'submit': self.login
        }))
