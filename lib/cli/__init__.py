import sys

from lib.cli.import_csv import import_employees, import_receipts, import_timesheets

COMMANDS = {
    'import_employees': {
        'method': import_employees,
        'args': 1
    },
    'import_receipts': {
        'method': import_receipts,
        'args': 1
    },
    'import_timesheets': {
        'method': import_timesheets,
        'args': 1
    },
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

