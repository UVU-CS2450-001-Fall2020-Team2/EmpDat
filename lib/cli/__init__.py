import sys

from lib.cli.import_csv import import_csv

COMMANDS = {
    'import_csv': {
        'method': import_csv,
        'args': 1
    }
}


def dispatch_cmd():
    args = sys.argv
    if len(args) < 2:
        return False
    cmd = args[1]

    if cmd not in COMMANDS:
        raise NotImplementedError
    if len(args) < COMMANDS[cmd]['args']:
        raise ValueError('Missing 1 or more arguments')

    COMMANDS[cmd]['method'](*args[2:])

    return True

