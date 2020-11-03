import tkinter as tk

import ui


def open_window(cls):
    ui.store.TK_ROOT.destroy()
    ui.store.TK_ROOT = tk.Tk()
    ui.store.TK_ROOT.title('EmpDat')
    page = cls()
    ui.store.TK_ROOT.mainloop()