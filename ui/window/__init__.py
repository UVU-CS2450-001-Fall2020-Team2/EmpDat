"""
Generic Window base classes
"""
import tkinter
from tkinter import messagebox, Toplevel
from tkinter.filedialog import askopenfilename

from ttkthemes import ThemedStyle

import ui


class UsesDialog:
    """
    A helper class for use inside of the views
    """

    @classmethod
    def show_error(cls, title, message, **options):
        """
        Helper method for showing an error dialog
        Calls tkinter.messagebox.showerror
        :param title: Title
        :param message: Message
        :param options: Options
        :return: None
        """
        messagebox.showerror(title=title, message=message, **options)

    @classmethod
    def show_info(cls, title, message, **options):
        """
        Helper method for showing an info dialog
        Calls tkinter.messagebox.showinfo
        :param title: Title
        :param message: Message
        :param options: Options
        :return: None
        """
        messagebox.showinfo(title=title, message=message, **options)

    @classmethod
    def show_warning(cls, title, message, **options):
        """
        Helper method for showing an warning dialog
        Calls tkinter.messagebox.showwarning
        :param title: Title
        :param message: Message
        :param options: Options
        :return: None
        """
        messagebox.showwarning(title=title, message=message, **options)

    @classmethod
    def show_file_picker(cls, title=None, filetypes=None):
        """
        Helper method for a file picker dialog
        :return: filepath selected
        """
        return askopenfilename(title=title, filetypes=filetypes)


class TkinterWindow(UsesDialog):
    """
    Easily creates windows and exposes event handlers for controllers
    """

    def __init__(self, event_handlers):
        """
        Creates a new Tkinter instance

        :param event_handlers: Received by the controller.
                                This contains hooks back to the controller for actions
        """
        self.master = tkinter.Tk()
        # self.master.configure(bg='white')
        style = ThemedStyle(self.master)
        style.theme_use('arc')

        try:
            self.master.iconphoto(True, ui.load_image("ui/icons/EmpDat.gif"))
        except tkinter.TclError:
            pass

        self.event_handlers = event_handlers

    def mainloop(self):
        """
        Forwards mainloop call to the Tkinter instance

        :return: None
        """
        self.master.mainloop()

    def destroy(self):
        """
        Destroys tkinter instance

        :return: None
        """
        self.master.destroy()


class TkinterDialog(Toplevel, UsesDialog):
    """
    Easily creates windows and exposes event handlers for controllers
    """

    def __init__(self, event_handlers):
        """
        A TkinterDialog is different as it uses a pre-existing Tkinter instance.

        :param event_handlers: Received by the controller.
                                This contains hooks back to the controller for actions
        """
        super().__init__()

        self.event_handlers = event_handlers
