"""
Login GUI Window implemented with Tkinter w/ built-in tester
"""
from tkinter.ttk import Frame, Label, Entry, Button

import ui
from ui.window import TkinterWindow


class LoginWindow(TkinterWindow):
    """
    Login GUI Window
    """

    def __init__(self, event_handlers):
        """Have a username, password, and submit button"""
        super().__init__(event_handlers)

        self.master.title("EmpDat Login")
        self.master.resizable(False, False)

        main = Frame(self.master)

        icon_image = ui.load_image("ui/icons/EmpDat.gif")
        icon = Label(main, image=icon_image)
        icon.image = icon_image
        icon.pack(padx=10, pady=10)

        self.title = Label(main, text="EmpDat")
        self.title.pack(pady=10)

        self.username = Label(main, text="Employee ID")
        self.entry = Entry(main, width=50)
        self.username.pack()
        self.entry.pack(padx=10)

        self.password = Label(main, text="Password")
        self.password_entry = Entry(main, width=50, show="•")
        self.password.pack()
        self.password_entry.pack(padx=10)

        self.submit_button = Button(
            main,
            text="Submit",
            command=lambda: event_handlers['submit'](self.entry.get(), self.password_entry.get()),
        )
        self.submit_button.pack(pady=10)

        main.pack()

        self.master.bind('<Return>',
                         lambda x: event_handlers['submit'](self.entry.get(),
                                                            self.password_entry.get())
                         )

    def validate(self):
        """
        Validates login fields
        :return: bool is_valid
        """
        if len(self.entry.get()) <= 0:
            self.show_error('Username required', 'No username given.')
            return False
        return True


if __name__ == '__main__':
    login_page = LoginWindow({
        'submit': lambda x, y: print('submitted! received:', x, y)
    })
    login_page.mainloop()
