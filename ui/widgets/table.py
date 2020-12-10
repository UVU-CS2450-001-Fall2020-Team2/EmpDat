# pylint: skip-file

"""
Customizations to tkintertable
"""
import math
from tkinter import END, StringVar, Menu
from tkinter.ttk import Entry, OptionMenu

from tkcalendar import DateEntry
from tkintertable import TableCanvas, Formula

from lib.repository.validator import is_valid_against


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

        col_name = self.model.getColumnName(col)

        if col_name in self.col_modifiers and 'render_as' in self.col_modifiers[col_name]:
            celltxt = self.col_modifiers[col_name]['render_as'](celltxt)
        if len(celltxt) == 0 or celltxt == 'None':
            celltxt = ''

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

        col_name = self.model.getColumnName(col)

        if self.read_only or (col_name in self.col_modifiers and
                              'read_only' in self.col_modifiers[col_name]
                              and self.col_modifiers[col_name]['read_only']):
            return
        # absrow = self.get_AbsoluteRow(row)
        height = self.rowheight
        model = self.getModel()
        cellvalue = self.model.getCellRecord(row, col)
        if Formula.isFormula(cellvalue):
            return
        else:
            text = self.model.getValueAt(row, col)
        if text == 'None':
            text = ''
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
            if not isinstance(e, str) and e.keysym == 'Return':
                self.delete('entry')
                # self.drawRect(row, col)
                # self.gotonextCell(e)
            if self.on_change:
                self.on_change()
            if len(self.unsaved) > 0:
                self.on_unsaved(False, row, col)
            else:
                self.on_unsaved(True, row, col)

            is_required = True if col_name in self.col_modifiers and \
                                  'required' in self.col_modifiers[col_name] else False
            if col_name in self.col_modifiers and 'validator' in self.col_modifiers[col_name]:
                if not is_required and value == '':
                    self.model.setColorAt(row, col, 'white')
                    self.redrawCell(row, col)
                    return

                if callable(self.col_modifiers[col_name]['validator']):
                    if not self.col_modifiers[col_name]['validator'](value):
                        self.model.setColorAt(row, col, 'coral')
                        self.redrawCell(row, col)
                else:
                    if not is_valid_against(self.col_modifiers[col_name]['validator'], value):
                        self.model.setColorAt(row, col, 'coral')
                        self.redrawCell(row, col)
            return

        if col_name in self.col_modifiers and 'options' in self.col_modifiers[col_name]:
            options = list(self.col_modifiers[col_name]['options'])

            if cellvalue in options:
                first = cellvalue
                options.remove(first)
                options.insert(0, first)

            self.cellentry = OptionMenu(self.parentframe, txtvar, *options,
                                        command=callback)
        elif col_name in self.col_modifiers and 'date' in self.col_modifiers[col_name]:
            self.cellentry = DateEntry(self.parentframe, width=20,
                                       textvariable=txtvar,
                                       takefocus=1,
                                       font=self.thefont)
            self.cellentry.bind('<<DateEntrySelected>>', callback)
        else:
            self.cellentry = Entry(self.parentframe, width=20,
                                   textvariable=txtvar,
                                   takefocus=1,
                                   font=self.thefont)
            self.cellentry.selection_range(0, END)

        try:
            self.cellentry.icursor(END)
        except AttributeError:
            pass
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

    def popupMenu(self, event, rows=None, cols=None, outside=None):
        """Add left and right click behaviour for canvas, should not have to override
            this function, it will take its values from defined dicts in constructor"""

        defaultactions = {"Set Fill Color": lambda: self.setcellColor(rows, cols, key='bg'),
                          "Set Text Color": lambda: self.setcellColor(rows, cols, key='fg'),
                          "Copy": lambda: self.copyCell(rows, cols),
                          "Paste": lambda: self.pasteCell(rows, cols),
                          "Fill Down": lambda: self.fillDown(rows, cols),
                          "Fill Right": lambda: self.fillAcross(cols, rows),
                          "Add Row(s)": lambda: self.addRows(),
                          "Delete Row(s)": lambda: self.deleteRow(),
                          "View Record": lambda: self.getRecordInfo(row),
                          "Clear Data": lambda: self.deleteCells(rows, cols),
                          "Select All": self.select_All,
                          "Auto Fit Columns": self.autoResizeColumns,
                          "Filter Records": self.showFilteringBar,
                          "New": self.new,
                          "Load": self.load,
                          "Save": self.save,
                          "Import text": self.importTable,
                          "Export csv": self.exportTable,
                          "Plot Selected": self.plotSelected,
                          "Plot Options": self.plotSetup,
                          "Export Table": self.exportTable,
                          "Preferences": self.showtablePrefs,
                          "Formulae->Value": lambda: self.convertFormulae(rows, cols)}

        main = ["Set Fill Color", "Set Text Color", "Copy", "Paste", "Fill Down", "Fill Right",
                "Clear Data"]
        general = ["Select All", "Auto Fit Columns", "Filter Records", "Preferences"]

        def createSubMenu(parent, label, commands):
            menu = Menu(parent, tearoff=0)
            popupmenu.add_cascade(label=label, menu=menu)
            for action in commands:
                menu.add_command(label=action, command=defaultactions[action])
            return menu

        def add_commands(fieldtype):
            """Add commands to popup menu for column type and specific cell"""
            functions = self.columnactions[fieldtype]
            for f in functions.keys():
                func = getattr(self, functions[f])
                popupmenu.add_command(label=f, command=lambda: func(row, col))
            return

        popupmenu = Menu(self, tearoff=0)

        def popupFocusOut(event):
            popupmenu.unpost()

        if outside == None:
            # if outside table, just show general items
            row = self.get_row_clicked(event)
            col = self.get_col_clicked(event)
            coltype = self.model.getColumnType(col)

            def add_defaultcommands():
                """now add general actions for all cells"""
                for action in main:
                    if action == 'Fill Down' and (rows == None or len(rows) <= 1):
                        continue
                    if action == 'Fill Right' and (cols == None or len(cols) <= 1):
                        continue
                    else:
                        popupmenu.add_command(label=action, command=defaultactions[action])
                return

            if coltype in self.columnactions:
                add_commands(coltype)
            add_defaultcommands()

        for action in general:
            popupmenu.add_command(label=action, command=defaultactions[action])

        popupmenu.add_separator()
        # createSubMenu(popupmenu, 'File', filecommands)
        # createSubMenu(popupmenu, 'Plot', plotcommands)
        popupmenu.bind("<FocusOut>", popupFocusOut)
        popupmenu.focus_set()
        popupmenu.post(event.x_root, event.y_root)
        return popupmenu

    # def deleteRowByRecname(self, recname):
    #     """Delete a row"""
    #     row = self.get
    #     self.model.deleteRow(row)
    #     self.setSelectedRow(row-1)
    #     self.clearSelected()
    #     self.redrawTable()
