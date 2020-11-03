import tkinter as tk

class Login:
    def __init__(self,gui):
        """Have a title, username, password, and submit button"""
        """Submit button will call submit method to login"""
        self.gui = gui
        self.greeting = tk.Label(text="Login")
        self.greeting.pack()
        #pack method organizes the item on the GUI

        self.username = tk.Label(text="Username")
        self.entry = tk.Entry(bg="orange", width=50)
        self.username.pack()
        self.entry.pack()

        self.password = tk.Label(text="Password")
        self.password_entry = tk.Entry(bg="orange", width=50, show='*')
        self.password.pack()
        self.password_entry.pack()

        self.submit_button = tk.Button(
            gui,
            text="Submit",
            width=35,
            height=2,
            fg="orange",
            #command = self.submit (Call submit method to login user)
        )
        self.submit_button.pack()

    def submit(self):
        """This will login the user"""
        

root = tk.Tk()
root.title("Login")
login_page = Login(root)
root.mainloop()
#This method will loop forever, waiting for events from the user, until the user exits the program – 
#either by closing the window, or by terminating the program with a keyboard interrupt in the console.