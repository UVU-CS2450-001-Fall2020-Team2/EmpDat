# pylint: skip-file

"""
Customizations to tkintertable
"""
import math
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
        if len(celltxt) == 0 or celltxt == 'None':
            celltxt = 'Not set'

        self.delete('celltext' + str(col) + '_' + str(row))
        h = self.rowheight
        x1, y1, x2, y2 = self.getCellCoords(row, col)
        w = x2 - x1
        wrap = False
        pad = 5
        # If celltxt is a number then we make it a string
        if type(celltxt) is float or type(celltxt) is int:
            celltxt = str(celltxt)
        length = len(celltxt)
        if length == 0:
            return
        # if cell width is less than x, print nothing
        if w <= 10:
            return

        if fgcolor == None or fgcolor == "None":
            fgcolor = 'black'
        if align == None:
            align = 'w'
        if align == 'w':
            x1 = x1 - w / 2 + pad
        elif align == 'e':
            x1 = x1 + w / 2 - pad

        if w < 18:
            celltxt = '.'
        else:
            fontsize = self.fontsize
            colname = self.model.getColumnName(col)
            # scaling between canvas and text normalised to about font 14
            scale = 8.5 * float(fontsize) / 12
            size = length * scale
            if size > w:
                newlength = w / scale
                # print w, size, length, newlength
                celltxt = celltxt[0:int(math.floor(newlength))]

        # if celltxt is dict then we are drawing a hyperlink
        if self.isLink(celltxt) == True:
            haslink = 0
            linktext = celltxt['text']
            if len(linktext) > w / scale or w < 28:
                linktext = linktext[0:int(w / fontsize * 1.2) - 2] + '..'
            if celltxt['link'] != None and celltxt['link'] != '':
                f, s = self.thefont
                linkfont = (f, s, 'underline')
                linkcolor = 'blue'
                haslink = 1
            else:
                linkfont = self.thefont
                linkcolor = fgcolor

            rect = self.create_text(x1 + w / 2, y1 + h / 2,
                                    text=linktext,
                                    fill=linkcolor,
                                    font=linkfont,
                                    tag=('text', 'hlink', 'celltext' + str(col) + '_' + str(row)))
            if haslink == 1:
                self.tag_bind(rect, '<Double-Button-1>', self.check_hyperlink)

        # just normal text
        else:
            rect = self.create_text(x1 + w / 2, y1 + h / 2,
                                    text=celltxt,
                                    fill=fgcolor,
                                    font=self.thefont,
                                    anchor=align,
                                    tag=('text', 'celltext' + str(col) + '_' + str(row)))
        return

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
