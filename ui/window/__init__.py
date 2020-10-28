"""
Generic Window base classes
"""
from tkinter import Toplevel


class View(Toplevel):
    """
    Easily creates windows and exposes event handlers for controllers
    """

    def __init__(self, tk_root, event_handlers):
        """

        :param tk_root: Root Tkinter instance
        :param event_handlers:
        """
        super().__init__(master = tk_root)

        self.event_handlers = event_handlers