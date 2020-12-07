# pylint: skip-file

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

    def __init__(self, *args, col_modifiers: dict = None, on_change=None,
                 on_unsaved=None, on_selected=None, **kwargs):
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
        :param on_change: callback called on every change
        :param on_unsaved: callback called on every change, passes 1 parameter
                            on whether there are pending changes
        :param on_selected: callback called on when a row is selected
        :param kwargs: blanket passthrough
        """
        super().__init__(*args, **kwargs)

        self.col_modifiers = col_modifiers
        self.unsaved = set()
        self.on_change = on_change
        self.on_unsaved = on_unsaved
        self.on_selected = on_selected

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
        height = self.rowheight
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
            if self.on_change:
                self.on_change()
            if len(self.unsaved) > 0:
                self.on_unsaved(False)
            else:
                self.on_unsaved(True)
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
                                           width=w - self.inset * 2, height=height - self.inset * 2,
                                           window=self.cellentry, anchor='nw',
                                           tag='entry')

        return

    def handle_left_click(self, event):
        """Respond to a single press"""

        self.on_selected()
        super().handle_left_click(event)

    # def deleteRowByRecname(self, recname):
    #     """Delete a row"""
    #     row = self.get
    #     self.model.deleteRow(row)
    #     self.setSelectedRow(row-1)
    #     self.clearSelected()
    #     self.redrawTable()
