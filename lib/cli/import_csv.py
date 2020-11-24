import csv
import os

from lib.model.employee import Employee


def import_csv(filename: str):
    if not os.path.exists(filename):
        raise ValueError('File given does not exist!')
    if not _is_csv(filename):
        raise ValueError('File given is not a valid CSV!')

    print('Importing from file', filename)

    i = 0
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        cursor = 0
        for row in reader:
            if cursor == 0:  # this row is the column names, unneeded
                cursor += 1
                continue
            else:
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
                    'classification_id': row[6],
                    'paymethod_id': row[7],
                    'salary': row[8],
                    'hourly_rate': row[9],
                    'commission_rate': row[10],
                    'bank_routing': row[11],
                    'bank_account': row[12],
                }))

                print('Importing Emp#', row[0])
                i += 1

    print(f'Imported {i} employees successfully')


def _split_names(full_name: str):
    split = full_name.split(" ")
    if len(split) == 3:
        return split[0] + ' ' + split[1], split[2]
    else:
        return split[0], split[1]


def _is_csv(infile):
    return True
    # csv_fileh = open(infile, 'rb')
    # try:
    #     dialect = csv.Sniffer().sniff(csv_fileh.read(1024))
    #     csv_fileh.seek(0)
    #     return True
    # except csv.Error:
    #     return False
