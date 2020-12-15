"""
Utility methods for backend
"""
import datetime
from _sha256 import sha256

from lib import HASH_SALT


def sha_hash(string) -> str:
    """
    Simplifies making a SHA 256 digest with a hash
    :param string: to hash
    :return: hashed str
    """
    return str(sha256((string + HASH_SALT).encode()).hexdigest())


def date_converter(date_thing):
    """
    Helper for model field caster. Converts a date of some string or date to datetime.date
    :param date_thing: date of type unknown
    :return: Date object
    """
    if not date_thing or date_thing == 'None':
        return None
    if isinstance(date_thing, datetime.date):
        return date_thing
    if isinstance(date_thing, str):
        try:
            return datetime.datetime.strptime(date_thing, '%m/%d/%y').date()
        except:
            return datetime.datetime.strptime(date_thing, '%Y-%m-%d').date()
    raise ValueError(f'Invalid date "{date_thing}" given')
