"""
Controller base classes
"""


class Controller:  # pylint: disable=too-few-public-methods
    """
    Sets the main structure for all UI Controllers
    """

    def __init__(self, view):
        """
        Every controller as a view attached
        :param view: TkinterWindow or TkinterFrame
        """
        self.view = view

    def show(self):
        """
        Controls presentation

        By default calls tkinter.mainloop()
        :return: None
        """
        self.view.mainloop()
