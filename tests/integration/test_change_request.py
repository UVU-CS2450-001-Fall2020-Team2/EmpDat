import datetime
import os
import time

from lib.layer.security import SecurityLayer, SecurityException, ChangeRequestException
from lib.model.employee import Employee
from lib.repository.db import database_setup

if __name__ == '__main__':
    database_setup({
        'DB_URL': 'sqlite+pysqlite:///empdat.db'
    })

    try:
        data = {
            'password': 'test',
            'social_security_number': '',
            'user_group_id': 0,
            'department_id': 0,
            'role': 'Accounting',
            'last_name': 'doe',
            'first_name': 'john',
            'start_date': datetime.date.today(),
            'date_of_birth': datetime.date.today(),
            'sex': 0,
            'address_line1': 'Test Street',
            'city': 'Test City',
            'state': 'Test State',
            'zipcode': '0000',
            'classification_id': 0,
            'paymethod_id': 0,
            'salary': 1.0
        }
        mymodel = Employee(data)
        saved = Employee.create(mymodel)

        security_layer = SecurityLayer(saved)

        saved.salary = 2.0
        saved.hourly_rate = 10
        try:
            Employee.update(saved)
            print('Changed w/o change request')
            assert False
        except SecurityException as e:
            print(e)
            assert False
        except ChangeRequestException as e:
            print('change request entered!')
            print(e.request.changes)

            assert True

    finally:
        time.sleep(1)
        os.remove("empdat.db")
