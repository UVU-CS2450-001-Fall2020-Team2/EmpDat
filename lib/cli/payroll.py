"""
Manages payroll
"""
import datetime

from lib.model.employee import Employee, MailMethod, DirectMethod


def run_payroll(output_filepath: str):
    """
    Runs payroll
    :param output_filepath: file output
    :return: None
    """
    employees = Employee.read_all()
    now = datetime.datetime.now()
    timestamp = now.strftime('%d-%m-%Y %H:%M')
    with open(output_filepath, 'a') as file:
        for employee in employees:
            balance = employee.get_balance()

            if balance > 0:
                if employee.payment_method.name == MailMethod.name:
                    file.write(f"[{timestamp}] Mail {balance:.2f} to "
                            f"{employee.get_name()} to "
                            f"{employee.address_line1} {employee.city} {employee.zipcode}\n")
                elif employee.payment_method.name == DirectMethod.name:
                    file.write(f"[{timestamp}] Transfer {balance:.2f} to "
                               f"{employee.get_name()} to "
                               f"{employee.address_line1} {employee.city} {employee.zipcode}\n")
