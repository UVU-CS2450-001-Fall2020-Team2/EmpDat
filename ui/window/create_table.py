from tkinter import *
  
class CreateTable: 
    def __init__(self,root,emp_list): 
        self.emp_list = emp_list
        #num of columns will stay the same due to the headers already being created
        self.TOTAL_COLUMNS = 10
        #get number of rows we need
        self.total_rows = len(self.emp_list)
        #self.edit = PhotoImage(file = "EmpDat/ui/window/edit.png")  
        # Creating a photoimage object to use image 
        # code for creating table 
        for i in range(self.total_rows): 
            for j in range(self.TOTAL_COLUMNS):
                if (j < self.TOTAL_COLUMNS - 2):
                    self.e = Label(root, width=10, text = self.emp_list[i][j], font=('Arial',17,))
                    self.e.grid(row=i, column=j) 
                """ else:
                    self.e = Button(root, text="Edit", image = self.edit)
                    self.e.grid(row=i, column=j)  """
                 
                

if __name__ == "__main__":
    # create root window 
    lst = [(12345,'John Doe','4435 South Happy Way','SLC', 'UT',84044,'Salary',1), 
        (12345,'John Doe','4435 South Happy Way','SLC', 'UT',84044,'Salary',1),
        (12345,'John Doe','4435 South Happy Way','SLC', 'UT',84044,'Salary',1),
        (12345,'John Doe','4435 South Happy Way','SLC', 'UT',84044,'Salary',1),
        (12345,'John Doe','4435 South Happy Way','SLC', 'UT',84044,'Salary',1)] 
    root = Tk() 
    t = CreateTable(root,lst) 
    root.mainloop() 
        