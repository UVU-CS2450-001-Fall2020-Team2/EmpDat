"""
Contains all the validation logic for the backend
"""
import re
from abc import abstractmethod


class ValidationException(Exception):
    """
    Thrown when a validation rule is violated
    """

    def __init__(self, message, database_field, *args):
        super().__init__(message, *args)
        self.database_field = database_field


class HasValidation:
    """
    Trait that adds validation to Models
    """

    def __setattr__(self, key, value):
        """
        This overrides when 'myobject.mykey' is set when the 'mykey' attribute doesn't exist
        This will run the value being set through a validator

        :param key: field to set
        :param value: value to set to field
        :return: None
        """
        if key == 'data':
            for data_key, data_value in value.items():
                if not self.validate(data_key, data_value):
                    raise ValidationException(f'{data_key} given is invalid', data_key)
            super().__setattr__(key, value)
        else:
            if self.validate(key, value):
                super().__setattr__(key, value)
            else:
                raise ValidationException(f'{key} given is invalid', key)

    def validate(self, key, new_value):
        """
        Validates a property using the field_validators dict
        :param key: property name.
            Models can specify the field_validators dict
            to tie properties to certain validation rules
        :param new_value:
        :return: True if new_value is valid
        """
        if self.field_validators and key in self.field_validators:
            return is_valid_against(self.field_validators[key], new_value)
        if self.field_optional_validators and key in self.field_optional_validators:
            if new_value and new_value != '' and new_value != 'None':
                return is_valid_against(self.field_optional_validators[key], new_value)
        return True

    @property
    @classmethod
    @abstractmethod
    def field_validators(cls) -> dict:
        """
        The field_validators dictionary specifies validation
        rules for model properties
        It is recommended to set this as a class-wide variable.
        Must be a dictionary.

        Example:
        field_validators = {
            'myfield': 'phone'
        }
        """
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def field_optional_validators(cls) -> dict:
        """
        The field_validators dictionary specifies validation
        rules for model properties
        It is recommended to set this as a class-wide variable.
        Must be a dictionary.

        These fields can also be blank

        Example:
        field_optional_validators = {
            'myfield': 'phone'
        }
        """
        raise NotImplementedError


def is_valid_against(validator_rule, value):
    """
    Called by HasValidation.validate to properly dispatch
    the validation rule to the method needed
    :param validator_rule: rule string
    :param value: new value
    :return: bool
    """
    if isinstance(validator_rule, list):
        return _generic_regex(validator_rule, value)
    if callable(validator_rule):
        return validator_rule(value)
    if validator_rule not in _validators:
        raise NotImplementedError("Validator Type does not exist")
    return _validators[validator_rule](value)


def _generic_regex(regexes: list, value):
    """
    A generic regex validator.

    Note that re.match returns the match or None instead
    of True or False.

    :param regexes: list of Regular Expressions to match
    :param value: value to check against
    :return: if value matches the regexes given
    """
    if isinstance(regexes, str):
        return re.match(re.compile(regexes), value) is not None

    for regex in regexes:
        result = re.match(re.compile(regex), str(value))
        if result is None:
            return None

    return True


def _phone_number(value):
    """
    Validates fields to be phone number formats only

    :param value:
    :return: if string is alphabetic
    """
    return _generic_regex([r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'], value)


def _alpha(value: str):
    """
    Validates fields to be alphabetic only

    :param value:
    :return: if string is alphabetic
    """
    return _generic_regex([r'^[A-Za-z\.\s]+$'], value)


def _numeric(value: str):
    """
    Validates fields to be numeric only

    :param value:
    :return: if string is alphabetic
    """
    return _generic_regex([r'^[0-9\-\.]+$'], value)


def _notnull(value):
    """
    Ensure the field is not null
    :param value:
    :return: if not null
    """
    return value is not None


def _password(value):
    """
    Enforces a password policy of:
        - at least 9 characters total
        - 1 lowercase letter
        - 1 uppercase
        - 1 number
        - 1 symbol
    :param value:
    :return: if acceptable
    """
    return _generic_regex([r'(?=.{9,})(?=.*?[^\w\s])(?=.*?[0-9])(?=.*?[A-Z]).*?[a-z].*'], value)


def _ssn(value):
    """
    Validates a field to match the US Social Security Number convention

    :param value:
    :return: if acceptable
    """
    return _generic_regex(
        [r'^(?!000)(?!666)(?!9[0-9][0-9])\d{3}[- ]?(?!00)\d{2}[- ]?(?!0000)\d{4}$'],
        value)


def _state_code(value):
    """
    Checks if a state code is valid

    :param value: state code
    :return: if valid US state code
    """
    return value in ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                     "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                     "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                     "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                     "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "INVALID"]


def _role(value):
    """
    Checks if a role is valid

    :param value: role
    :return: if valid role
    """
    # TODOFuture fix me, this shouldn't be hardcoded
    return value in ['Viewer', 'Accounting', 'Reporter', 'Admin']


def _email(value):
    """
    Validates a field for an email

    :param value: email
    :return: if acceptable
    """
    return _generic_regex([r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'], value)


def _bank_routing(value):
    """
    Validates a field for a bank routing number

    :param value: bank route
    :return: if acceptable
    """
    return _generic_regex([r'^[0-9\-\.A-Za-z\s]+$'], value)


def _date(value):
    """
    Validates a field for a bank routing number

    :param value: bank route
    :return: if acceptable
    """
    return _generic_regex([r'\d{1,2}\/\d{1,2}\/\d{2,4}'], value)


_validators = {
    'phone': _phone_number,
    'alpha': _alpha,
    'numeric': _numeric,
    'notnull': _notnull,
    'password': _password,
    'ssn': _ssn,
    'state_code': _state_code,
    'role': _role,
    'email': _email,
    'date': _date,
    'bank_routing': _bank_routing
}
