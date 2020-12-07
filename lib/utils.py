"""
Utility methods for backend
"""

from _sha256 import sha256

from lib import HASH_SALT


def sha_hash(string) -> str:
    """
    Simplifies making a SHA 256 digest with a hash
    :param string: to hash
    :return: hashed str
    """
    return str(sha256((string + HASH_SALT).encode()).hexdigest())
