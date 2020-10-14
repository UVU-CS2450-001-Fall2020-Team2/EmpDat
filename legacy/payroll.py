"""I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part,
constitutes cheating, and that I will receive a zero on this project
if I am found in violation of this policy."""

from abc import ABC, abstractmethod
import os, shutil

employees = []
pay_logfile = "paylog.txt"


class Employee:
    """
    Employee class, creates Employee object which is mutable

    All parameters must be passed in to create new instance of Employee object
    """
    def __init__(
        self,
        emp_id,
        name,
        address,
        city,
        state,
        zipcode,
        classnum,
        paymeth,
        sal,
        hour,
        comm,
        route,
        acc
        ):
        '''
        Employee constructor
        :param emp_id: Employee's ID Number
        :param name: Employee's Name
        :param address: Employee's Address
        :param city: Employee's City
        :param zipcode: Employee's Zipcode
        :param classnum: Employee's Classification Number
        :param paymeth: Employee's Payment Method(DirectMethod or MailMethod)
        :param hour: Hourly Employee
        :param sal: Salaried Employee
        :param comm: Commissioned Employee
        :param route: Routing Number (DirectMethod payment)
        :param acc: Bank Account Number (DirectMethod payment)
        :param classification: Employee Classification (Hourly, Salary, Commission)
        :param paymethod: Direct deposit or Mailed Payment

        '''
        self.emp_id = emp_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.classnum = classnum
        self.paymeth = paymeth
        self.hour = hour
        self.sal = sal
        self.comm = comm
        self.route = route
        self.acc = acc
        self.classification = self.get_emp_class()
        self.paymethod = self.get_emp_paymeth()

    def change_emp_class(self, clas):
        '''
        This method changes the employee payment classification number
        :param clas: classification number
        :return: classification number
        '''
        self.classnum = clas
        return self.classnum

    def make_salaried(self, sal):
        '''
        This method changes employee classification to Salaried
        :param sal: salary ammount
        :return: classification (Hourly, Salary, Commissioned)
        '''
        self.classification = Salaried(self, sal)
        return self.classification

    def get_emp_class(self):
        '''
        This method returns employees classification number.
        :param: self
        :return: 1 = Hourly, 2 = Salaried, 3 = commissioned
        '''
        num = int(self.classnum)
        if num == 1:
            return Hourly(self, self.hour)
        elif num == 2:
            return Salaried(self, self.sal)
        else:
            return Commissioned(self, self.sal, self.comm)

    def get_emp_paymeth(self):
        '''
        This method returns employee payment method
        :param: self
        :return: bool If DirectMethod returns routing # and account #, Else returns MailMethod
        '''
        num = int(self.paymeth)
        if num == 1:
            return DirectMethod(self, self.route, self.acc)
        else:
            return MailMethod(self)

    def make_hourly(self, hr):
        '''
        This Method sets Employee classification to hourly
        :param hr: hourly wage (float)
        :return: returns hourly employee classification
        '''
        self.classification = Hourly(self, hr)
        return self.classification

    def make_commissioned(self, comm, rcpt):
        '''
        This method sets Employee classsification to Commissioned
        :param comm: commission ammount(float)
        :param rcpt: list containing reciepts
        :return: employee classification
        '''
        self.classification = Commissioned(self, comm, rcpt)
        return self.classification

    def direct_method(self, route, acc):
        '''
        This method sets employee payment method to direct deposit
        :param route: routing number(int)
        :param acc: account number(int)
        :return: employee payment method
        '''
        self.paymethod = DirectMethod(self, route, acc)
        return self.paymethod


class Classification(ABC):
    '''
    Abstract class of Employee classification

    Creates the abstract issue payment method which is used for all employee classifications
    '''
    def __init__(self, employee):
        '''
        Constructor for Classification
        :param employee: creates instance of employee
        '''
        self.emp = employee

    @abstractmethod
    def issue_payment(self):
        '''
        Abstract Method to issue payments
        '''
        pass


class Commissioned(Classification):
    '''
    Class for hourly employee, inherits from classification to use abstract issue payment method
    '''
    def __init__(self, employee, salary, comm):
        '''
        This method is the constructor to make employee commissioned
        :param employee: instance of Employee class(uses super)
        :param salary: salary ammount paid to employee
        :param comm: commission percentage
        '''
        super().__init__(employee)
        self.commission = float(comm)
        self.salary = float(salary)
        self.rcpt_list = []

    def issue_payment(self):
        '''
        This method issues payment to commission class employee
        :param self:
        :return: money paid to employee
        '''
        money = self.salary / 24
        s = sum(self.rcpt_list)
        money += s * (self.commission / 100)
        self.rcpt_list = []
        return money

    def add_receipt(self, rcpt):
        '''
        This method is used to add a new reciept
        :param rcpt: add list containing receipts which is converted to float points
        '''
        self.rcpt_list.append(float(rcpt))


class Hourly(Classification):
    '''
    Class for hourly employee, inherits from classification to use abstract issue payment method
    '''
    def __init__(self, employee, hr):
        '''
        This method is the constructor for the Hourly classification
        :param employee: employee object
        :param hr: Hourly wage ammount paid to employee
        '''
        super().__init__(employee)
        self.hourly_rate = float(hr)
        self.time_list = []

    def issue_payment(self):
        '''
        This method issues payment to hourly classification
        :returns: money paid to hourly employee
        '''
        money = 0
        s = sum(self.time_list)
        money += self.hourly_rate * s
        self.time_list = []
        return money

    def add_timecard(self, time):
        '''
        This method is used to add a new time card to hourly employee
        :param time: List of hours worked
        '''
        self.time_list.append(time)


class Salaried(Classification):
    '''
    Class for salary employee, inherits from classification to use abstract issue payment method
    '''
    def __init__(self, employee, sal):
        '''
        This method is the constructor for the Salaried classification
        :param employee: employee object
        :param sal: Salary ammount paid to employee
        '''
        self.emp = employee
        self.sal = sal

    def issue_payment(self):
        '''
        This method issues salaried employee payment
        :return: Returns Bimonthly payment(float)
        '''
        return float(self.sal) / 24


class PaymentMethod(ABC):
    '''
    Abstract payment class, allows for each employee to have a payment method that can be issued
    '''
    def __init__(self, paymeth):
        '''
        This method is the constructor for the paymethod
        :param paymeth: Direct or Mail method
        '''
        self.paymet = paymeth

    @abstractmethod

    def issue(self):
        '''
        Abstract method for issuing payments
        '''
        pass


class MailMethod(PaymentMethod):
    '''
    Direct method payment class, inherits from PaymentMethod to use abstract issue method
    '''
    def __init__(self, employee):
        '''
        This method is the constructor
        :param employee: instance of Employee class
        '''
        self.employee = employee

    def issue(self):
        '''
        This method prints out the mailed payment method issued payment being mailed to employee
        '''
        self.employee
        global pay_logfile
        with open(pay_logfile, "a") as f:
            text = "Mailing {0:.2f} to {1} at {2} {3} {4} \n".format(
                self.employee.classification.issue_payment(),
                self.employee.name,
                self.employee.address,
                self.employee.city,
                self.employee.zipcode,
            )
            f.write(text)


class DirectMethod(PaymentMethod):
    '''
    Direct method payment class, inherits from PaymentMethod to use abstract issue method
    '''
    def __init__(self, employee, route, acc):
        '''
        This method is the constructor
        :param employee: instance of Employee class
        :param route: Bank routing number
        :param acc: Bank account number
        '''
        self.acc = acc
        self.route = route
        self.employee = employee

    def issue(self):
        '''
        This method prints out the direct payment method issued payment being mailed to employee
        '''
        global pay_logfile
        with open(pay_logfile, "a") as f:
            text = "Transferred {0:.2f} for {1} to {2} {3} \n".format(
                self.employee.classification.issue_payment(),
                self.employee.name,
                self.employee.acc,
                self.employee.route,
            )
            f.write(text)


def run_payroll():
    '''
    This method issues payments to employees in CSV file
    '''
    if os.path.exists(
        pay_logfile
    ):  # pay_log_file is a global variable holding ‘payroll.txt’
        os.remove(pay_logfile)
    for emp in employees:  # employees is the global list of Employee objects
        emp.paymethod.issue()  # issue_payment calls a method in the classification # object to compute the pay, which in turn invokes
        # the pay method.


def process_receipts():
    '''
    This method opens receipts file and processes receipts for commissioned employees
    '''
    with open("receipts.txt") as f:
        ln = f.readlines()
        for data in ln:
            ld_emp = data.rstrip("\n").split(",")
            emps = find_employee_by_id(ld_emp[0])
            i = 1
            while i < len(ld_emp):
                emps.classification.add_receipt(ld_emp[i])
                i += 1


def process_timecards():
    '''
    This method opens time card file and processes time cards for hourly employees
    '''
    with open("timecards.txt") as f:
        ln = f.readlines()
        for data in ln:
            ld_emp = data.rstrip("\n").split(",")
            emps = find_employee_by_id(ld_emp[0])

            i = 1
            while i < len(ld_emp):
                emps.classification.add_timecard(float(ld_emp[i]))
                i += 1


def load_employees():
    '''
    This method loads global employees from CSV file and creates employee objects passing data into
    Employee class
    '''
    global employees
    with open("employees.csv") as f:
        ln = f.readlines()[1::]
        for data in ln:
            ld_emp = data.rstrip("\n").split(",")
            emp = Employee(
                ld_emp[0],
                ld_emp[1],
                ld_emp[2],
                ld_emp[3],
                ld_emp[4],
                ld_emp[5],
                ld_emp[6],
                ld_emp[7],
                ld_emp[8],
                ld_emp[9],
                ld_emp[10],
                ld_emp[11],
                ld_emp[12],
            )
            employees.append(emp)


def find_employee_by_id(id):
    '''
    This method finds Employee by ID number
    :param id: This is the employee ID [0] from CSV file
    :return: returns Employee ID if found
    '''
    for emp in employees:
        if emp.emp_id == id:
            return emp


def main():
    '''
    This method is the main driver of the program. Creates Employee objects, processes hourly time cards
    processes commissioned receipts, issues payments to employees
    Creates files showing payments issued
    '''
    load_employees()

    process_timecards()

    process_receipts()
    run_payroll()

    # Save copy of payroll file
    shutil.copyfile("paylog.txt", "paylog1.txt")

    # Change Karina Gay to Salaried and DirectMethod by changing her Employee object:
    emp = find_employee_by_id("688997")
    emp.make_salaried(45884.99)
    emp.direct_method("30417353-K", "465794-3611")

    # Change TaShya Snow to Commissioned and MailMethod; add some receipts
    emp = find_employee_by_id("522759")
    emp.make_commissioned(50005.50, 25)
    emp.direct_method("30417353-K", "465794-3611")
    clas = emp.classification
    clas.add_receipt(1109.73)
    clas.add_receipt(746.10)

    # Change Rooney Alvarado to Hourly; add some hour entries
    emp = find_employee_by_id("165966")

    emp.make_hourly(21.53)

    clas = emp.classification

    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)

    # Rerun payroll
    run_payroll()


if __name__ == "__main__":
    main()
