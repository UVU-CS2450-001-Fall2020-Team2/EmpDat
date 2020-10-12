import re
from abc import abstractmethod


class HasValidation:

    def __setattr__(self, key, value):
        """
        This overrides when myobject.mykey is set when the mykey attribute doesn't exist
        This will run the value being set through a validator

        :param key: field to set
        :param value: value to set to field
        :return: None
        """
        if key == 'data':
            for data_key, data_value in value.items():
                if not self.validate(data_key, data_value):
                    raise ValueError(f'{data_key} given is invalid!')  # TODO make error message better
            super().__setattr__(key, value)
        else:
            if self.validate(key, value):
                super().__setattr__(key, value)
            else:
                # print('no validators')
                raise ValueError(f'{key} given is invalid!')  # TODO make error message better

    def validate(self, key, new_value):
        if self.field_validators and key in self.field_validators:
            if is_valid_against(self.field_validators[key], new_value):
                return True
            else:
                return False
        else:
            return True

    @property
    @classmethod
    @abstractmethod
    def field_validators(cls) -> dict:
        """
        It is recommended to set this as a class-wide variable.
        Must be a dictionary.

        Example:
        field_validators = {
            'myfield': 'phone'
        }
        """
        raise NotImplementedError


def is_valid_against(validator_type, value):
    if isinstance(validator_type, list):
        _generic_regex(validator_type, value)
    else:
        if validator_type not in _validators:
            raise NotImplementedError("Validator Type does not exist")
        else:
            return _validators[validator_type](value)


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
    return _generic_regex(['^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'], value)


def _alpha(value: str):
    """
    Validates fields to be alphabetic only

    :param value:
    :return: if string is alphabetic
    """
    return _generic_regex(['^[A-Za-z]+$'], value)


def _notnull(value):
    return value is not None


_validators = {
    'phone': _phone_number,
    'alpha': _alpha,
    'notnull': _notnull
}
