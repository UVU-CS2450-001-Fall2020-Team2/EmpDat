import os

from lib.layer.security import SecurityLayer
from lib.model.employee import Employee
from lib.repository.db import database_setup

if __name__ == '__main__':
    database_setup({
        'DB_URL': 'sqlite+pysqlite:///empdat.db'
    })

    data = {
        'last_name': 'doe',
        'role': 'Viewer'
    }
    mymodel = Employee(data)
    # print(mymodel.data)

    mymodel.first_name = 'john'
    # print(mymodel.to_dict())

    saved = Employee.create(mymodel)
    security_layer = SecurityLayer(saved)
    # Employee.destroy('XYZ')

    test = Employee.read(saved.id)
    # print(test.to_dict())

    test2 = Employee.read_all()
    print(test2)
    print('---')

    test3 = Employee.read_by(filters={
        'role': [('=', 'Viewer')]
    })
    print(test3)
    for row in test3:
        print(row.__dict__)

    os.remove("empdat.db")
