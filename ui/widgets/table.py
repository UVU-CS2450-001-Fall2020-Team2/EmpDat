"""
Customizations to tkintertable
"""
from tkinter import END, StringVar
from tkinter.ttk import Entry, Combobox

from tkintertable import TableCanvas, Formula


class EmpDatTableCanvas(TableCanvas):
    """
    Override for TableCanvas
    """

    def __init__(self, *args, col_modifiers: dict = None, **kwargs):
        """
        TableCanvas constructor
        :param args: blanket passthrough
        :param col_modifiers: dictionary modifying column entry
            Example:
                {
                    0: {
                        'read_only': True
                    },
                    1: {
                        'options': ['A', 'B', 'C"]  # Options A, B, and C
                    },
                    2: {
                        'render_as': lambda X: Y    # Render X as Y
                    }
                }

        :param kwargs: blanket passthrough
        """
        super().__init__(*args, **kwargs)

        self.col_modifiers = col_modifiers
        self.unsaved = set()

    def drawText(self, row, col, celltxt, fgcolor=None, align=None):
        """Draw the text inside a cell area"""

        if col in self.col_modifiers and 'render_as' in self.col_modifiers[col]:
            celltxt = self.col_modifiers[col]['render_as'](celltxt)

        super().drawText(row, col, celltxt, fgcolor, align)

    def drawCellEntry(self, row, col, text=None):
        """When the user single/double clicks on a text/number cell, bring up entry window"""

        if self.read_only or (col in self.col_modifiers and
                              'read_only' in self.col_modifiers[col]
                              and self.col_modifiers[col]['read_only']):
            return
        # absrow = self.get_AbsoluteRow(row)
        h = self.rowheight
        model = self.getModel()
        cellvalue = self.model.getCellRecord(row, col)
        if Formula.isFormula(cellvalue):
            return
        else:
            text = self.model.getValueAt(row, col)
        x1, y1, x2, y2 = self.getCellCoords(row, col)
        w = x2 - x1
        # Draw an entry window
        txtvar = StringVar()
        txtvar.set(text)

        def callback(e):
            value = txtvar.get()
            if value == '=':
                # do a dialog that gets the formula into a text area
                # then they can click on the cells they want
                # when done the user presses ok and its entered into the cell
                self.cellentry.destroy()
                # its all done here..
                self.formula_Dialog(row, col)
                return

            coltype = self.model.getColumnType(col)
            if coltype == 'number':
                sta = self.checkDataEntry(e)
                if sta == 1:
                    self.unsaved.add(self.model.getRecName(row))
                    model.setValueAt(value, row, col)
            elif coltype == 'text':
                self.unsaved.add(self.model.getRecName(row))
                model.setValueAt(value, row, col)

            color = self.model.getColorAt(row, col, 'fg')
            self.drawText(row, col, value, color, align=self.align)
            if e.keysym == 'Return':
                self.delete('entry')
                # self.drawRect(row, col)
                # self.gotonextCell(e)
            return

        if col in self.col_modifiers and 'options' in self.col_modifiers[col]:
            options = self.col_modifiers[col]['options']

            self.cellentry = Combobox(self.parentframe, width=20,
                                      textvariable=txtvar,
                                      takefocus=1,
                                      font=self.thefont)
            self.cellentry['values'] = options
            self.cellentry.bind('<<ComboboxSelected>>', callback)
        else:
            self.cellentry = Entry(self.parentframe, width=20,
                                   textvariable=txtvar,
                                   # bg=self.entrybackgr,
                                   # relief=FLAT,
                                   takefocus=1,
                                   font=self.thefont)

        self.cellentry.icursor(END)
        self.cellentry.bind('<Return>', callback)
        self.cellentry.bind('<KeyRelease>', callback)
        self.cellentry.focus_set()
        self.entrywin = self.create_window(x1 + self.inset, y1 + self.inset,
                                           width=w - self.inset * 2, height=h - self.inset * 2,
                                           window=self.cellentry, anchor='nw',
                                           tag='entry')

        return

    # def deleteRowByRecname(self, recname):
    #     """Delete a row"""
    #     row = self.get
    #     self.model.deleteRow(row)
    #     self.setSelectedRow(row-1)
    #     self.clearSelected()
    #     self.redrawTable()
