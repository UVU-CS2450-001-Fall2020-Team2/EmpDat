from lib.model.employee import Employee
from lib.repository.db import database_setup

if __name__ == '__main__':
    database_setup({
        'DB_URL': 'sqlite+pysqlite:///empdat.db'
    })


    data = {
        'id': 'XYZ'
    }
    mymodel = Employee(data)
    print(mymodel.to_dict())

    Employee.create(mymodel)