import logging
import re
import sys

from argparse import ArgumentParser, ArgumentTypeError
from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal

from hnbex import commands
from hnbex.api import ApiError
from hnbex.commands import CommandError
from hnbex.output import print_err


Command = namedtuple("Command", ["name", "description", "arguments"])

CLIENT_WEBSITE = 'https://github.com/ihabunek/hnbex-cli'


def date_type(value):
    if value.lower() == 'today':
        return date.today()

    if value.lower() == 'tomorrow':
        return date.today() + timedelta(days=1)

    try:
        value = datetime.strptime(value, "%Y-%m-%d").date()
    except:
        raise ArgumentTypeError(f"Invalid date '{value}'")

    return value


def decimal_type(value):
    try:
        return Decimal(value)
    except:
        raise ArgumentTypeError(f"Invalid decimal value '{value}'")


def currency_type(value):
    if not re.match("^[a-z]{3}$", value, re.IGNORECASE):
        raise ArgumentTypeError(f"Invalid currency code '{value}'")

    return value.upper()


RANGE_ARGS = [
    (["-e", "--end"], {
        "help": "the last day of the range (defaults to tomorrow)",
        "type": date_type,
        "default": date.today() + timedelta(days=1),
    }),
    (["-s", "--start"], {
        "help": "the first day of the range (default calculated as `end - days`)",
        "type": date_type,
    }),
    (["-d", "--days"], {
        "help": "number of days in the range (defaults to 30)",
        "type": int,
        "default": 30
    }),
]


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
        ] + RANGE_ARGS,
    ),
    Command(
        name="chart",
        description="Draw exchange rate chart for a single currency",
        arguments=[
            (["currency"], {
                "help": "the currency code, e.g. USD",
                "type": currency_type,
            }),
            (["-t", "--template"], {
                "help": "GnuPlot script template to use (qt is graphical, dumb is textual)",
                "choices": ["qt", "dumb"],
                "type": str,
                "default": "dumb",
            }),
        ] + RANGE_ARGS,
    ),
    Command(
        name="convert",
        description="Convert between currencies",
        arguments=[
            (["amount"], {
                "help": "the amount to convert",
                "type": decimal_type,
            }),
            (["source_currency"], {
                "help": "currency from which to convert",
                "type": currency_type,
            }),
            (["target_currency"], {
                "help": "currency code to which to convert (defaults to EUR)",
                "type": currency_type,
                "default": "EUR",
                "nargs": "?",
            }),
            (["-d", "--date"], {
                "help": "the lookup date (defaults to today)",
                "type": date_type,
                "default": date.today(),
            }),
            (["-v", "--value-only"], {
                "help": "output only the conversion result, no verbose output",
                "action": 'store_true',
                "default": False,
            }),
            (["-p", "--precision"], {
                "help": "number of decimals to round the resulting value (defaults to 2)",
                "type": int,
                "default": 2,
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
    }),
    (["--debug"], {
        "help": "log HTTP requests",
        "action": 'store_true',
        "default": False,
    })
]


def get_parser():
    description = "Exhange rates published by the Croatian National Bank (HNB)."
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
    if "--debug" in sys.argv:
        logging.basicConfig(level=logging.DEBUG)

    parser = get_parser()
    args = parser.parse_args()

    if "func" not in args:
        parser.print_help()
        return

    try:
        args.func(**args.__dict__)
    except CommandError as e:
        print_err(str(e))
        sys.exit(1)
    except ApiError as e:
        print_err(str(e))
        sys.exit(1)
