"""
Login GUI Window implemented with Tkinter w/ built-in tester
"""
import tkinter as tk

from ui.window import View


class LoginWindow(View):
    """
    Login GUI Window
    """

    def __init__(self, tk_root, event_handlers):
        """Have a username, password, and submit button"""
        super().__init__(tk_root, event_handlers)
        self.master.title("EmpDat Login")

        self.username = tk.Label(text="Username")
        self.entry = tk.Entry(bg="orange", width=50)
        self.username.pack()
        self.entry.pack()

        self.password = tk.Label(text="Password")
        self.password_entry = tk.Entry(bg="orange", width=50, show="•")
        self.password.pack()
        self.password_entry.pack()

        self.submit_button = tk.Button(
            self.master,
            text="Submit",
            width=35,
            height=2,
            fg="orange",
            command=lambda: event_handlers['submit'](self.entry.get(), self.password_entry.get())
        )
        self.submit_button.pack()


if __name__ == '__main__':
    root = tk.Tk()
    login_page = LoginWindow(root, {
        'submit': lambda x, y: print('submitted! received:', x, y)
    })
    root.mainloop()
