"""I declare that the following source code was written solely by me. 
I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project 
if I am found in violation of this policy."""

from abc import ABC, abstractmethod
import os, shutil

employees = []
pay_logfile = "paylog.txt"


class Employee:
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
        acc,
    ):
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
        self.classnum = clas
        return self.classnum

    def make_salaried(self, sal):
        self.classification = Salaried(self, sal)
        return self.classification

    def get_emp_class(self):
        num = int(self.classnum)
        if num == 1:
            return Hourly(self, self.hour)
        elif num == 2:
            return Salaried(self, self.sal)
        else:
            return Commissioned(self, self.sal, self.comm)

    def get_emp_paymeth(self):
        num = int(self.paymeth)
        if num == 1:
            return DirectMethod(self, self.route, self.acc)
        else:
            return MailMethod(self)

    def make_hourly(self, hr):
        self.classification = Hourly(self, hr)
        return self.classification

    def make_commissioned(self, comm, rcpt):
        self.classification = Commissioned(self, comm, rcpt)
        return self.classification

    def direct_method(self, route, acc):
        self.paymethod = DirectMethod(self, route, acc)
        return self.paymethod


class Classification(ABC):
    def __init__(self, employee):
        self.emp = employee

    @abstractmethod
    def issue_payment(self):
        pass


class Commissioned(Classification):
    def __init__(self, employee, salary, comm):
        super().__init__(employee)
        self.commission = float(comm)
        self.salary = float(salary)
        self.rcpt_list = []

    def issue_payment(self):
        money = self.salary / 24
        s = sum(self.rcpt_list)
        money += s * (self.commission / 100)
        self.rcpt_list = []
        return money

    def add_receipt(self, rcpt):
        self.rcpt_list.append(float(rcpt))


class Hourly(Classification):
    def __init__(self, employee, hr):
        super().__init__(employee)
        self.hourly_rate = float(hr)
        self.time_list = []

    def issue_payment(self):
        money = 0
        s = sum(self.time_list)
        money += self.hourly_rate * s
        self.time_list = []
        return money

    def add_timecard(self, time):
        self.time_list.append(time)


class Salaried(Classification):
    def __init__(self, employee, sal):
        self.emp = employee
        self.sal = sal

    def issue_payment(self):
        return float(self.sal) / 24


class PaymentMethod(ABC):
    def __init__(self, paymeth):
        self.paymet = paymeth

    @abstractmethod
    def issue(self):
        pass


class MailMethod(PaymentMethod):
    def __init__(self, employee):
        self.employee = employee

    def issue(self):
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
    def __init__(self, employee, route, acc):
        self.acc = acc
        self.route = route
        self.employee = employee

    def issue(self):
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
    if os.path.exists(
        pay_logfile
    ):  # pay_log_file is a global variable holding ‘payroll.txt’
        os.remove(pay_logfile)
    for emp in employees:  # employees is the global list of Employee objects
        emp.paymethod.issue()  # issue_payment calls a method in the classification # object to compute the pay, which in turn invokes
        # the pay method.


def process_receipts():
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
    for emp in employees:
        if emp.emp_id == id:
            return emp


def main():
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
