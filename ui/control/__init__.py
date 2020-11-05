class Controller:
    """
    docstring
    """

    def __init__(self, view):
        self.view = view

    def show(self):
        self.view.mainloop()
