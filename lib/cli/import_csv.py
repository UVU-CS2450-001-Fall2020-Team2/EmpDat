"""
Import CSV library
"""
import csv
import datetime
import os
from tkinter import messagebox

from lib.model.employee import Employee
from lib.model.receipt import Receipt
from lib.model.timesheet import TimeSheet


def _import_csv(filepath: str, has_headers=False):
    if not os.path.exists(filepath):
        raise ValueError('File given does not exist!')
    if not _is_csv(filepath):
        raise ValueError('File given is not a valid CSV!')

    print('Importing from file', filepath)

    i = 0
    with open(filepath, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        cursor = 0
        for row in reader:
            if cursor == 0 and has_headers:  # this row is the column names, unneeded
                cursor += 1
                continue
            yield row
            i += 1


def import_receipts(filepath: str, from_cmd=True):
    """
    Imports Receipts in the following format:

    [employee ID],[receipt amount],[receipt amount], ...

    Example:
        160769,63.02,163.42,140.06,84.15
        377013,220.89,238.57,218.84


    :param filepath: path to file
    :param from_cmd: bool if calling from cmd line
    :return: None
    """
    employees_not_found = []

    i = 0
    for row in _import_csv(filepath):
        employee_id = int(row[0])

        if not Employee.read(employee_id):
            print(f'No Employee#{employee_id} exists, ignoring')
            employees_not_found.append(employee_id)
            continue

        receipts = row[1:]

        for receipt in receipts:
            Receipt.create(Receipt({
                'user_id': employee_id,
                'amount': receipt
            }))
            print('Importing Receipt#', i, 'for Emp#', employee_id)
            i += 1

    print(f'Imported {i} receipts successfully')
    if not from_cmd:
        if len(employees_not_found) > 0:
            messagebox.showinfo("showwarning", f'Imported {i} receipts '
            f'successfully. However, the following'
            f'employee ID\'s were not found: {employees_not_found}')
        else:
            messagebox.showinfo("showinfo", f'Imported {i} receipts successfully')


def import_timesheets(filepath: str, from_cmd=True):
    """
    Imports Timesheets in the following format:

    [employee ID],[time in hours],[time in hours], ...

    Example:
        426824,7.4,6.5,5.7,8.0,6.9,7.5,6.5,7.5
        934003,5.8,7.5,5.8,4.8,5.9,4.8,4.0,6.6,5.5,7.2

    :param filepath: path to file
    :param from_cmd: bool if calling from cmd line
    :return: None
    """
    employees_not_found = []

    i = 0
    for row in _import_csv(filepath):
        employee_id = int(row[0])

        if not Employee.read(employee_id):
            print(f'No Employee#{employee_id} exists, ignoring')
            employees_not_found.append(employee_id)
            continue

        timesheets = row[1:]

        for time_in_hours in timesheets:
            datetime_end = datetime.datetime.now()
            datetime_begin = datetime_end - datetime.timedelta(
                seconds=(float(time_in_hours) * 3600)
            )

            TimeSheet.create(TimeSheet({
                'user_id': employee_id,
                'datetime_end': datetime_end,
                'datetime_begin': datetime_begin
            }))
            print('Importing TimeSheet#', i, 'for Emp#', employee_id)
            i += 1

    print(f'Imported {i} timesheets successfully')
    if not from_cmd:
        if len(employees_not_found) > 0:
            messagebox.showinfo("showwarning", f'Imported {i} timesheets successfully. '
            f'However, the following'
            f'employee ID\'s were not found: {employees_not_found}')
        else:
            messagebox.showinfo("showinfo", f'Imported {i} timesheets successfully')


def import_employees(filename: str, from_cmd=True):
    """
    Imports Employees in the following format:

    ID,Name,Address,City,State,Zip,Classification,PayMethod,Salary,Hourly,Commission,Route,Account

    with headers included

    Example:
        ID,Name,Address,City,State,Zip,Classification,PayMethod,Salary,Hourly,Commission,Route,Account  # pylint: disable=line-too-long
        688997,Karina Gay,998 Vitae St.,Atlanta,GA,45169,1,1,45884.99,46.92,34,30417353-K,465794-3611  # pylint: disable=line-too-long

    :param filepath: path to file
    :param from_cmd: bool if calling from cmd line
    :return: None
    """
    i = 0
    for row in _import_csv(filename, has_headers=True):
        names = _split_names(row[1])
        Employee.create(Employee({
            'id': row[0],
            'role': 'Viewer',
            'first_name': names[0],
            'last_name': names[1],
            'address_line1': row[2],
            'address_line2': '',
            'city': row[3],
            'state': row[4],
            'zipcode': row[5],
            'classification_id': int(row[6]),
            'paymethod_id': int(row[7]),
            'salary': row[8],
            'hourly_rate': row[9],
            'commission_rate': row[10],
            'bank_routing': row[11],
            'bank_account': row[12],
        }))
        print('Importing Emp#', row[0])
        i += 1

    print(f'Imported {i} employees successfully')
    if not from_cmd:
        messagebox.showinfo("showinfo", f'Imported {i} employees successfully')


def _split_names(full_name: str):
    split = full_name.split(" ")
    if len(split) == 3:
        return split[0] + ' ' + split[1], split[2]
    return split[0], split[1]


def _is_csv(infile):  # pylint: disable=unused-argument
    return True
    # csv_fileh = open(infile, 'rb')
    # try:
    #     dialect = csv.Sniffer().sniff(csv_fileh.read(1024))
    #     csv_fileh.seek(0)
    #     return True
    # except csv.Error:
    #     return False
