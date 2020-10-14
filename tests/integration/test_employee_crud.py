import os

from lib.model.employee import Employee
from lib.repository.db import database_setup

if __name__ == '__main__':
    database_setup({
        'DB_URL': 'sqlite+pysqlite:///empdat.db'
    })

    data = {
        'id': 'XYZ',
        'last_name': 'doe'
    }
    mymodel = Employee(data)
    # print(mymodel.data)
    mymodel.first_name = 'john'
    # print(mymodel.to_dict())

    Employee.create(mymodel)
    # Employee.destroy('XYZ')

    test = Employee.read('XYZ')
    # print(test.to_dict())

    test2 = Employee.read_all()
    print(test2)
    print('---')

    test3 = Employee.read_by(filters={
        'first_name': [('!=', 'john')]
    })
    print(test3)

    os.remove("empdat.db")
