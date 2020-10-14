"""
Contains all the validation logic for the backend
"""
import re
from abc import abstractmethod


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
                    # TODO make error message better
                    raise ValueError(f'{data_key} given is invalid!')
            super().__setattr__(key, value)
        else:
            if self.validate(key, value):
                super().__setattr__(key, value)
            else:
                # print('no validators')
                # TODO make error message better
                raise ValueError(f'{key} given is invalid!')

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
        result = re.match(re.compile(regex), value)
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
    return _generic_regex([r'^[A-Za-z]+$'], value)


def _notnull(value):
    """
    Ensure the field is not null
    :param value:
    :return: if not null
    """
    return value is not None


_validators = {
    'phone': _phone_number,
    'alpha': _alpha,
    'notnull': _notnull
}
