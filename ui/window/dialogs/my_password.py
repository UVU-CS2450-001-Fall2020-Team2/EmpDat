"""
View for changing one's own password
"""
from tkinter.ttk import Label, Entry, Button

from ui.window import TkinterDialog


class MyPasswordDialog(TkinterDialog):
    """
    Dialog for changing your own password
    """

    def __init__(self, event_handlers):
        """
        Shows the a password and password confirm fields

        :param event_handlers: Expects 'save'
        """
        super().__init__(event_handlers)

        Label(self, text="Old Password").grid(column=0, row=0)
        self.old_pass_entry = Entry(self, show="•")
        self.old_pass_entry.grid(column=1, row=0)

        Label(self, text="New Password").grid(column=0, row=1)
        self.password_entry = Entry(self, show="•")
        self.password_entry.grid(column=1, row=1)

        Label(self, text="Confirm Password").grid(column=0, row=2)
        self.confirm_password_entry = Entry(self, show="•")
        self.confirm_password_entry.grid(column=1, row=2)

        Label(self, text="Passwords need to include one number, one "
                         "capital letter, and one special character") \
            .grid(column=0, row=3, columnspan=2)

        # Actions
        self.save_btn = Button(self, text="Save",
                               command=lambda: self.event_handlers['save'](
                                   self,
                                   self.old_pass_entry.get(),
                                   self.password_entry.get(),
                                   self.confirm_password_entry.get()
                               ))
        self.save_btn.grid(column=0, row=4)
        self.cancel_btn = Button(self, text="Cancel", command=self.destroy)
        self.cancel_btn.grid(column=1, row=4)

        self.master.bind('<Return>', lambda: self.event_handlers['save'](
            self,
            self.old_pass_entry.get(),
            self.password_entry.get(),
            self.confirm_password_entry.get()
        ))
