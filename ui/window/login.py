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
        """Have a title, username, password, and submit button"""
        super().__init__(tk_root, event_handlers)
        self.title = "Login Page"
        self.greeting = tk.Label(text="Login")
        self.greeting.pack()
        # pack method organizes the item on the GUI

        self.username = tk.Label(text="Username")
        self.entry = tk.Entry(bg="orange", width=50)
        self.username.pack()
        self.entry.pack()

        self.password = tk.Label(text="Password")
        self.password_entry = tk.Entry(bg="orange", width=50)
        self.password.pack()
        self.password_entry.pack()

        self.submit_button = tk.Button(
            tk_root,
            text="Submit",
            width=35,
            height=2,
            fg="orange",
            # command = self.submit (Call submit method to login user)
        )
        self.submit_button.pack()


if __name__ == '__main__':
    root = tk.Tk()
    login_page = LoginWindow(root, {})
    root.mainloop()
