"""
Generic Window base classes
"""
import tkinter
from tkinter import messagebox, Toplevel

from ttkthemes import ThemedStyle


class UsesDialog:

    def show_error(self, title, message, **options):
        """
        Helper method for showing an error dialog
        Calls tkinter.messagebox.showerror
        :param title: Title
        :param message: Message
        :param options: Options
        :return: None
        """
        messagebox.showerror(title=title, message=message, **options)

    def show_info(self, title, message, **options):
        """
        Helper method for showing an info dialog
        Calls tkinter.messagebox.showinfo
        :param title: Title
        :param message: Message
        :param options: Options
        :return: None
        """
        messagebox.showinfo(title=title, message=message, **options)

    def show_warning(self, title, message, **options):
        """
        Helper method for showing an warning dialog
        Calls tkinter.messagebox.showwarning
        :param title: Title
        :param message: Message
        :param options: Options
        :return: None
        """
        messagebox.showwarning(title=title, message=message, **options)


class TkinterWindow(UsesDialog):
    """
    Easily creates windows and exposes event handlers for controllers
    """

    def __init__(self, event_handlers):
        """
        :param event_handlers:
        """
        self.master = tkinter.Tk()
        # self.master.configure(bg='white')
        style = ThemedStyle(self.master)
        style.theme_use('arc')

        self.event_handlers = event_handlers

    def mainloop(self):
        self.master.mainloop()

    def destroy(self):
        self.master.destroy()


class TkinterFrame(Toplevel, UsesDialog):
    """
    Easily creates windows and exposes event handlers for controllers
    """

    def __init__(self, event_handlers):
        """
        :param event_handlers:
        """
        super().__init__()

        self.event_handlers = event_handlers
