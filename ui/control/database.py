from ui.control import Controller
from ui.window.database import DatabaseWindow


class DatabaseController(Controller):

    def __init__(self):
        super().__init__(DatabaseWindow({
            # 'submit': self.login
        }))

    def show(self):
        self.view.setup_grid()
        super().show()
