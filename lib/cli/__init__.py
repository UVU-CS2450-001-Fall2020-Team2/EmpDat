"""
The root of the command line interface for EmpDat
"""

import sys

from lib.cli.import_csv import import_employees, import_receipts, import_timesheets
from lib.cli.payroll import run_payroll

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
    'run_payroll': {
        'method': run_payroll,
        'args': 1
    }
}


def dispatch_cmd():
    """
    The EmpDat main script will call this when an argument is given
    :return: bool if command succeeded
    """

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
