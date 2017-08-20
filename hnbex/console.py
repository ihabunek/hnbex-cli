# -*- coding: utf-8 -*-

import re
import sys

from argparse import ArgumentParser, ArgumentTypeError
from collections import namedtuple
from datetime import date, datetime

from hnbex import commands
from hnbex.output import print_err


Command = namedtuple("Command", ["name", "description", "arguments"])

CLIENT_WEBSITE = 'https://github.com/ihabunek/hnbex-cli'


def date_type(value):
    if value.lower() == 'today':
        return date.today()

    try:
        value = datetime.strptime(value, "%Y-%m-%d").date()
    except:
        raise ArgumentTypeError("Invalid date '{}'".format(value))

    return value


def currency_type(value):
    if not re.match("^[a-z]{3}$", value, re.IGNORECASE):
        raise ArgumentTypeError("Invalid currency code '{}'".format(value))

    return value.upper()


COMMANDS = [
    Command(
        name="daily",
        description="Show daily exchange rates for all currencies",
        arguments=[
            (["date"], {
                "help": "the lookup date",
                "nargs": "?",
                "type": date_type,
                "default": date.today(),
            }),
        ],
    ),
    Command(
        name="range",
        description="Show exchange rates for a single currency in the given date range",
        arguments=[
            (["currency"], {
                "help": "the currency code, e.g. USD",
                "type": currency_type,
            }),
            (["end_date"], {
                "help": "the end date (defaults to today)",
                "nargs": "?",
                "type": date_type,
                "default": date.today(),
            }),
            (["start_date"], {
                "help": "the start date (defaults to 30 days before the end date)",
                "nargs": "?",
                "type": date_type,
            }),
        ],
    ),
]


# Arguments used on every command
COMMON_ARGS = [
    (["--no-color"], {
        "help": "don't use ANSI colors in output",
        "action": 'store_true',
        "default": False,
    })
]


def get_parser():
    description = """
        Exhange rates for Croatian Kuna (HRK) published by the Croatian National Bank (HNB).
        Data fetched from hnb.ex, a service provided by Dobar Kod.
    """

    parser = ArgumentParser(prog='hnbex', description=description, epilog=CLIENT_WEBSITE)
    parser.add_argument('--no-color', action='store_true', help='don\'t use ANSI colors in output')

    subparsers = parser.add_subparsers(title="commands")

    for command in COMMANDS:
        sub = subparsers.add_parser(command.name, help=command.description)

        # Set the function to call to the function of same name in the "commands" package
        sub.set_defaults(func=commands.__dict__.get(command.name))

        for args, kwargs in command.arguments + COMMON_ARGS:
            sub.add_argument(*args, **kwargs)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if "func" not in args:
        parser.print_help()
        return

    try:
        args.func(**args.__dict__)
    except Exception as e:
        print_err(str(e))
        sys.exit(1)
