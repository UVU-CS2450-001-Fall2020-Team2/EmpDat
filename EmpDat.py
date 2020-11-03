"""
Main entry into the application
"""

import tkinter as tk

from ui.control.login import LoginController

if __name__ == '__main__':
    TK_ROOT = tk.Tk()
    login_page = LoginController()
    TK_ROOT.mainloop()
