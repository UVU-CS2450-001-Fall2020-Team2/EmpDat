"""
Login GUI Window implemented with Tkinter w/ built-in tester
"""
import tkinter as tk

from ui.window import *


class LoginWindow(TkinterWindow):
    """
    Login GUI Window
    """

    def __init__(self, event_handlers):
        """Have a username, password, and submit button"""
        super().__init__(event_handlers)

        self.master.title("EmpDat Login")

        self.title = tk.Label(bg="white", text="EmpDat", font=('Arial', 17), pady=15)
        self.title.pack()

        self.username = tk.Label(bg="white", text="Username", font=('Arial', 15))
        self.entry = tk.Entry(bg="white", width=50, font=('Arial', 17))
        self.username.pack()
        self.entry.pack()

        self.password = tk.Label(bg="white", text="Password", font=('Arial', 15))
        self.password_entry = tk.Entry(bg="white", width=50, show="•", font=('Arial', 17))
        self.password.pack()
        self.password_entry.pack()

        self.submit_button = tk.Button(
            self.master,
            text="Submit",
            width=35,
            height=2,
            fg="black",
            command=lambda: event_handlers['submit'](self.entry.get(), self.password_entry.get()),
            font=('Arial', 14),
        )
        self.submit_button.pack()

        self.master.configure(padx=20, pady=20)


if __name__ == '__main__':
    login_page = LoginWindow({
        'submit': lambda x, y: print('submitted! received:', x, y)
    })
    login_page.mainloop()
