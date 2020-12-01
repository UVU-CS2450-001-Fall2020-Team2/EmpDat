"""
Employee Data Model
"""
from abc import abstractmethod

from sqlalchemy import MetaData, Table, Column, String, DateTime, Float, Integer, Text, Date, BigInteger

from lib.model import DynamicViewModel, HasRelationships, register_database_model
from lib.model.receipt import Receipt
from lib.model.time_sheet import TimeSheet
from lib.repository.db import DatabaseRepository
from lib.utils import sha_hash


@register_database_model
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
        'id': lambda s: int(s),
        'salary': lambda s: float(s) if s is not None else None,
        'hourly_rate': lambda s: float(s) if s is not None else None,
        'commission_rate': lambda s: float(s) if s is not None else None,
        # 'start_date': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'date_of_birth': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'date_left': lambda d: datetime.date.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'created_at': lambda d: datetime.datetime.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
        # 'modified_at': lambda d: datetime.datetime.fromtimestamp(d),  # pylint: disable=unnecessary-lambda
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
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def from_view_model(cls, view_model: dict):
        employee = Employee.read(int(view_model[cls.view_columns['id']]))
        for key, value in cls.view_columns.items():
            if value in view_model:
                setattr(employee, key, view_model[value])

        employee.cast_fields()

        print(employee)

        employee.classification = Classification.to_enum_from_name(employee.classification)
        employee.classification_id = employee.classification.get_id()
        employee.payment_method = PaymentMethod.to_enum_from_name(employee.payment_method)
        employee.paymethod_id = employee.payment_method.get_id()

        print(employee)

        return employee

    @classmethod
    def authenticate(cls, username, password):
        employees = Employee.read_by(filters={
            'id': int(username)
        })

        if len(employees) < 1:
            return None

        employee = employees[0]

        if sha_hash(password) == employee.password:
            return employee
        return None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
    classifications.append(cls)
    classifications_dict[cls.name] = {
        'class': cls,
        'id': len(classifications)
    }
    return cls


def register_payment_method(cls):
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

    def __init__(self):
        pass

    @abstractmethod
    def issue_payment(self, **kwargs):
        """
        Abstract Method to issue payments
        """
        raise NotImplementedError

    def __str__(self):
        return self.name

    @classmethod
    def from_enum(cls, id):
        return classifications[id - 1]()

    @classmethod
    def to_enum(cls, clz):
        return classifications[classifications_dict[clz.name]['id']]

    @classmethod
    def to_enum_from_name(cls, name):
        return classifications[classifications_dict[name]['id'] - 1]

    @classmethod
    def get_id(cls):
        return classifications_dict[cls.name]['id']


@register_classification
class Hourly(Classification):
    """
    Class for hourly employee, inherits from classification to use abstract issue payment method
    """
    name = 'Hourly'

    def __init__(self):
        """
        This method is the constructor for the Hourly classification
        """
        super().__init__()

    def issue_payment(self, employee_id, hourly_rate):
        """
        This method issues payment to hourly classification
        :returns: money paid to hourly employee
        """
        money = 0

        timesheets = TimeSheet.read_by({
            'user_id': employee_id,
            'paid': ('!=', True)
        })
        s = sum([timesheet.to_hours() for timesheet in timesheets])
        money += hourly_rate * s

        for timesheet in timesheets:
            timesheet.paid = True
            TimeSheet.update(timesheet)

        return money

    # def add_timecard(self, time):
    #     """
    #     This method is used to add a new time card to hourly employee
    #     :param time: List of hours worked
    #     """
    #     self.time_list.append(time)


@register_classification
class Salaried(Classification):
    """
    Class for salary employee, inherits from classification to use abstract issue payment method
    """
    name = 'Salary'

    def __init__(self):
        """
        This method is the constructor for the Salaried classification
        """
        super().__init__()

    def issue_payment(self, salary):
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

    def __init__(self):
        """
        This method is the constructor to make employee commissioned
        :param employee: instance of Employee class(uses super)
        :param salary: salary ammount paid to employee
        :param comm: commission percentage
        """
        super().__init__()

    def issue_payment(self, employee_id, salary, commission):
        """
        This method issues payment to commission class employee
        :param commission:
        :param salary:
        :return: money paid to employee
        """
        money = salary / 24

        receipts = Receipt.read_by({
            'user_id': employee_id,
            'paid': ('!=', True)
        })
        s = sum([receipt.amount for receipt in receipts])
        money += s * (commission / 100)

        for receipt in receipts:
            receipt.paid = True
            Receipt.update(receipt)

        return money

    # def add_receipt(self, rcpt):
    #     """
    #     This method is used to add a new reciept
    #     :param rcpt: add list containing receipts which is converted to float points
    #     """
    #     self.rcpt_list.append(float(rcpt))


class PaymentMethod:
    """
    Abstract payment class, allows for each employee to have a payment method that can be issued
    """
    name: str = ''

    def __init__(self):
        """
        This method is the constructor for the paymethod
        """

    @abstractmethod
    def issue(self, employee: Employee):
        """
        Abstract method for issuing payments
        """
        raise NotImplementedError

    @classmethod
    def from_enum(cls, id):
        return pay_methods[id - 1]()

    @classmethod
    def to_enum(cls, clz):
        return pay_methods[pay_methods_dict[clz.name]['id']]

    @classmethod
    def to_enum_from_name(cls, name):
        return pay_methods[pay_methods_dict[name]['id'] - 1]

    @classmethod
    def get_id(cls):
        return pay_methods_dict[cls.name]['id']

    def __str__(self):
        return self.name


@register_payment_method
class DirectMethod(PaymentMethod):
    """
    Direct method payment class, inherits from PaymentMethod to use abstract issue method
    """
    name = 'Direct Deposit'

    def __init__(self):
        """
        This method is the constructor
        """
        super().__init__()

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

    def __init__(self):
        """
        This method is the constructor
        """
        super().__init__()

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
