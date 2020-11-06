from tkinter import *


class CreateTable:
    def __init__(self, root, emp_list):
        # self.emp_list = emp_list
        # num of columns will stay the same due to the headers already being created
        self.TOTAL_COLUMNS = 10
        # get number of rows we need
        # self.total_rows = len(self.emp_list)
        self.edit = PhotoImage(file="ui/icons/pencil.gif")
        self.delete = PhotoImage(file="ui/icons/trash.gif")
        # Creating a photoimage object to use image
        self.data = []

    def render_list(self, emp_list):
        total_rows = len(emp_list)
        self.data = []

        # code for creating table
        for i in range(total_rows):
            row = []
            for j in range(self.TOTAL_COLUMNS):
                if j < self.TOTAL_COLUMNS - 2:
                    e = Label(root, width=10, text=emp_list[i][j], font=('Arial', 17,))
                    e.grid(row=i, column=j)
                elif j == 8:
                    e = Button(root, text="Edit", image=self.edit, command=lambda: self.add_to_list(
                        (12345, 'John Wacky', '4435 South Happy Way', 'SLC', 'UT', 84044, 'Salary', 1)
                    ))
                    e.grid(row=i, column=j)
                else:
                    e = Button(root, text="Delete", image=self.delete, command=lambda: self.add_to_list(
                        (12345, 'John Wacky', '4435 South Happy Way', 'SLC', 'UT', 84044, 'Salary', 1)
                    ))
                    e.grid(row=i, column=j)
                row.append(e)
            self.data.append(row)

    def add_to_list(self, to_add):
        i = len(self.data) + 1
        row = []
        for j in range(self.TOTAL_COLUMNS):
            if j < self.TOTAL_COLUMNS - 2:
                e = Label(root, width=10, text=to_add[j], font=('Arial', 17,))
                e.grid(row=i, column=j)
            else:
                e = Button(root, text="Edit", image=self.edit, command=lambda: self.destroy_row(i))  # the 'i' preprogrammed here will shift whenever a row is deleted above it
                e.grid(row=i, column=j)
            row.append(e)
        self.data.append(row)

    def destroy_list(self):
        for i in self.data:
            for j in self.data[i]:
                self.data[i][j].destory()

    def destroy_row(self, row_number):
        for element in self.data[row_number]:
            element.destroy()


if __name__ == "__main__":
    # create root window 
    lst = [(12345, 'John Doe', '4435 South Happy Way', 'SLC', 'UT', 84044, 'Salary', 1),
           (12345, 'John Doe', '4435 South Happy Way', 'SLC', 'UT', 84044, 'Salary', 1),
           (12345, 'John Doe', '4435 South Happy Way', 'SLC', 'UT', 84044, 'Salary', 1),
           (12345, 'John Doe', '4435 South Happy Way', 'SLC', 'UT', 84044, 'Salary', 1),
           (12345, 'John Doe', '4435 South Happy Way', 'SLC', 'UT', 84044, 'Salary', 1)]
    root = Tk()
    t = CreateTable(root, lst)
    t.render_list(lst)
    root.mainloop()
