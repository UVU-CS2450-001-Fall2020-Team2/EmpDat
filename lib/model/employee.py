"""
Employee Data Model
"""
import datetime
from abc import abstractmethod

from sqlalchemy import MetaData, Table, Column, String, \
    DateTime, Float, Integer, Text, Date, BigInteger

from lib.model import DynamicViewModel, HasRelationships, register_database_model
from lib.model.receipt import Receipt
from lib.model.time_sheet import TimeSheet
from lib.repository.db import DatabaseRepository
from lib.utils import sha_hash


@register_database_model  # pylint: disable=too-many-ancestors
class Employee(DatabaseRepository, DynamicViewModel, HasRelationships):
    """
    Tied directly to the 'employee' table
    """
    resource_uri = 'employee'
    field_validators = {
        'id': 'numeric',
        'last_name': 'alpha',
        'first_name': 'alpha',
        # 'phone_number': 'phone',
        # 'emergency_contact_phone': 'phone',
    }
    view_columns = {
        'id': 'ID',
        'social_security_number': 'SSN',
        'role': 'Role',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'start_date': 'Start Date',
        'date_of_birth': 'DOB',
        'sex': 'Sex',
        'address_line1': 'Address',
        'address_line2': 'Apt, PO Box, etc.',
        'city': 'City',
        'state': 'State',
        'zipcode': 'Postal Code',
        'email': 'Email',
        'phone_number': 'Phone Number',
        'emergency_contact_name': 'Emergency Contact',
        'emergency_contact_relation': 'Emergency Contact Relation',
        'emergency_contact_phone': 'Emergency Contact Phone',
        'classification': 'Classification',
        'payment_method': 'Payment Method',
        'salary': 'Salary',
        'hourly_rate': 'Hourly Rate',
        'commission_rate': 'Commission Rate',
        'bank_routing': 'Bank Rounting',
        'bank_account': 'Bank Account',
        'timesheet': 'Timesheet',
        'date_left': 'Date Left',
        'notes': 'Notes',
    }
    field_casts = {
        'id': lambda s: int(s),  # pylint: disable=unnecessary-lambda
        'salary': lambda s: float(s) if s is not None else None,  # pylint: disable=unnecessary-lambda
        'hourly_rate': lambda s: float(s) if s is not None else None,  # pylint: disable=unnecessary-lambda
        'commission_rate': lambda s: float(s) if s is not None else None,  # pylint: disable=unnecessary-lambda
    }

    def __init__(self, data):
        DynamicViewModel.__init__(self, data)
        DatabaseRepository.__init__(self)

        self.load_relationships()

    def to_dict(self):
        return self.trim_relationships(DynamicViewModel.to_dict(self))

    def load_relationships(self):
        self.classification = Classification.from_enum(self.classification_id)
        self.payment_method = PaymentMethod.from_enum(self.paymethod_id)

    def relationship_fields(self):
        return [
            'classification',
            'payment_method'
        ]

    def get_name(self):
        """
        Returns the Employee first and last name
        :return: str
        """
        return f"{self.first_name} {self.last_name}"

    def get_balance(self):
        """
        Gets amount owed to employee. Ran during payroll
        :return: balance float
        """
        if self.classification.name == Hourly.name:
            return self.classification.issue_payment(self.id, self.hourly_rate)
        elif self.classification.name == Salaried.name:
            return self.classification.issue_payment(self.salary)
        elif self.classification.name == Commissioned.name:
            return self.classification.issue_payment(self.id, self.salary, self.commission_rate)
        return 0

    def get_payment_method(self):
        """
        Returns info for payment method
        :return: list
        """
        return self.payment_method.issue(self)

    def update_password(self, new_password: str):
        self.password = sha_hash(new_password)  # pylint: disable=attribute-defined-outside-init
        Employee.update(self)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def new_empty(cls):
        return Employee({
            'password': '',
            'role': 'Viewer',
            'first_name': 'required',
            'last_name': 'required',
            'user_group_id': 0,
            'start_date': datetime.date.today(),
            'date_of_dirth': datetime.date.today(),
            'sex': -1,
            'address_line1': 'required',
            'city': 'required',
            'state': 'required',
            'zipcode': 'required',
            'classification_id': 'required',
            'paymethod_id': 'required'
        })

    @classmethod
    def from_view_model(cls, view_model: dict):
        employee = Employee.read(int(view_model[cls.view_columns['id']]))
        for key, value in cls.view_columns.items():
            if value in view_model:
                setattr(employee, key, view_model[value])

        employee.cast_fields()

        employee.classification = Classification.to_enum_from_name(  # pylint: disable=attribute-defined-outside-init
            employee.classification)
        employee.classification_id = employee.classification.get_id()  # pylint: disable=attribute-defined-outside-init
        employee.payment_method = PaymentMethod.to_enum_from_name(  # pylint: disable=attribute-defined-outside-init
            employee.payment_method)
        employee.paymethod_id = employee.payment_method.get_id()  # pylint: disable=attribute-defined-outside-init

        return employee

    @classmethod
    def authenticate(cls, username, password):
        """
        Authenticates an employee as a user
        :param username: str
        :param password: str
        :return: Employee
        """
        employees = Employee.read_by(filters={
            'id': int(username)
        })

        if len(employees) < 1:
            return None

        employee = employees[0]

        if sha_hash(password) == employee.password:
            return employee
        return None

    @classmethod
    def table(cls, metadata=MetaData()):
        return Table(cls.resource_uri, metadata,
                     Column('id', BigInteger().with_variant(Integer, "sqlite"), primary_key=True),
                     Column('password', String(255)),
                     Column('social_security_number', String(12)),
                     Column('user_group_id', Integer),
                     Column('department_id', Integer),
                     Column('role', String(64)),
                     Column('last_name', String(64)),
                     Column('first_name', String(64)),
                     Column('start_date', Date),
                     Column('date_of_birth', Date),
                     Column('sex', Integer),
                     Column('address_line1', String(128)),
                     Column('address_line2', String(128), nullable=True),
                     Column('city', String(45)),
                     Column('state', String(45)),
                     Column('zipcode', String(16)),
                     Column('email', String(45), nullable=True),
                     Column('phone_number', String(45), nullable=True),
                     Column('emergency_contact_name', String(45), nullable=True),
                     Column('emergency_contact_relation', String(45), nullable=True),
                     Column('emergency_contact_phone', String(45), nullable=True),
                     Column('classification_id', Integer),
                     Column('paymethod_id', Integer),
                     Column('salary', Float, nullable=True),
                     Column('hourly_rate', Float, nullable=True),
                     Column('commission_rate', Float, nullable=True),
                     Column('bank_routing', String(32), nullable=True),
                     Column('bank_account', String(32), nullable=True),
                     Column('timesheet', Float, nullable=True),
                     Column('created_at', DateTime),
                     Column('modified_at', DateTime),
                     Column('date_left', Date, nullable=True),
                     Column('notes', Text, nullable=True),
                     extend_existing=True
                     )


classifications = []
pay_methods = []
classifications_dict = {}
pay_methods_dict = {}


def register_classification(cls):
    """
    Decorator that adds classification to the global registry
    :param cls: class
    :return: Class
    """
    classifications.append(cls)
    classifications_dict[cls.name] = {
        'class': cls,
        'id': len(classifications)
    }
    return cls


def register_payment_method(cls):
    """
    Decorator that adds payment method to the global registry
    :param cls: class
    :return: Class
    """
    pay_methods.append(cls)
    pay_methods_dict[cls.name] = {
        'class': cls,
        'id': len(pay_methods)
    }
    return cls


class Classification:
    """
    Abstract class of Employee classification

    Creates the abstract issue payment method which is used for all employee classifications
    """
    name: str = ''

    @abstractmethod
    def issue_payment(self, *args):
        """
        Abstract Method to issue payments
        """
        raise NotImplementedError

    def __str__(self):
        return self.name

    @classmethod
    def from_enum(cls, index):
        """
        Converts from the Classification ID to the classification instance
        :param index: int
        :return: class instance
        """
        return classifications[index - 1]()

    @classmethod
    def to_enum(cls, clz):
        """
        Converts from the classification instance to an ID
        :param clz: class instance
        :return: int
        """
        return classifications[classifications_dict[clz.name]['id']]

    @classmethod
    def to_enum_from_name(cls, name):
        """
        Converts from the classification class to the name
        :param clz: class
        :return: str
        """
        return classifications[classifications_dict[name]['id'] - 1]

    @classmethod
    def get_id(cls):
        """
        Gets the registered ID
        :return: ID int
        """
        return classifications_dict[cls.name]['id']


@register_classification
class Hourly(Classification):
    """
    Class for hourly employee, inherits from classification to use abstract issue payment method
    """
    name = 'Hourly'

    def issue_payment(self, employee_id, hourly_rate):  # pylint: disable=arguments-differ
        """
        This method issues payment to hourly classification
        :returns: money paid to hourly employee
        """
        money = 0

        timesheets = TimeSheet.read_by({
            'user_id': employee_id,
            'paid': False
        })
        total = sum([timesheet.to_hours() for timesheet in timesheets])
        money += hourly_rate * total

        for timesheet in timesheets:
            timesheet.paid = True
            TimeSheet.update(timesheet)

        return money


@register_classification
class Salaried(Classification):
    """
    Class for salary employee, inherits from classification to use abstract issue payment method
    """
    name = 'Salary'

    def issue_payment(self, salary):  # pylint: disable=arguments-differ
        """
        This method issues salaried employee payment
        :return: Returns Bimonthly payment(float)
        """
        return float(salary) / 24


@register_classification
class Commissioned(Classification):
    """
    Class for hourly employee, inherits from classification to use abstract issue payment method
    """
    name = 'Commission'

    def issue_payment(self, employee_id, salary, commission):  # pylint: disable=arguments-differ
        """
        This method issues payment to commission class employee
        :param commission:
        :param salary:
        :return: money paid to employee
        """
        money = salary / 24

        receipts = Receipt.read_by({
            'user_id': employee_id,
            'paid': False
        })
        total = sum([receipt.amount for receipt in receipts])
        money += total * (commission / 100)

        for receipt in receipts:
            receipt.paid = True
            Receipt.update(receipt)

        return money


class PaymentMethod:
    """
    Abstract payment class, allows for each employee to have a payment method that can be issued
    """
    name: str = ''

    @abstractmethod
    def issue(self, employee: Employee):
        """
        Abstract method for issuing payments
        """
        raise NotImplementedError

    @classmethod
    def from_enum(cls, index):
        """
        Converts from ID to class instance
        :param index: int
        :return: class instance
        """
        return pay_methods[index - 1]()

    @classmethod
    def to_enum(cls, clz):
        """
        Converts from class to ID
        :param clz: instance
        :return: id int
        """
        return pay_methods[pay_methods_dict[clz.name]['id']]

    @classmethod
    def to_enum_from_name(cls, name):
        """
        Converts from name to ID
        :param name: str
        :return: id int
        """
        return pay_methods[pay_methods_dict[name]['id'] - 1]

    @classmethod
    def get_id(cls):
        """
        Gets ID from current class
        :return: id int
        """
        return pay_methods_dict[cls.name]['id']

    def __str__(self):
        return self.name


@register_payment_method
class DirectMethod(PaymentMethod):
    """
    Direct method payment class, inherits from PaymentMethod to use abstract issue method
    """
    name = 'Direct Deposit'

    def issue(self, employee):
        """
        This method prints out the direct payment method issued payment being mailed to employee
        """
        return [
            employee.classification.issue_payment(),
            employee.first_name,
            employee.last_name,
            employee.bank_account,
            employee.bank_routing
        ]


@register_payment_method
class MailMethod(PaymentMethod):
    """
    Direct method payment class, inherits from PaymentMethod to use abstract issue method
    """
    name = 'Mail'

    def issue(self, employee):
        """
        This method prints out the mailed payment method issued payment being mailed to employee
        """
        return [
            employee.classification.issue_payment(),
            employee.first_name,
            employee.last_name,
            employee.address_line1,
            employee.address_line2,
            employee.city,
            employee.state,
            employee.zipcode
        ]
