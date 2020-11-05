from _sha256 import sha256

from lib import HASH_SALT


def sha_hash(string) -> str:
    return str(sha256((string + HASH_SALT).encode()).hexdigest())
