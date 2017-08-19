# -*- coding: utf-8 -*-

import re
import sys

from argparse import ArgumentParser, ArgumentTypeError
from collections import namedtuple
from datetime import date, datetime

from hnbex import commands
from hnbex.output import print_out, print_err
from hnbex.api import ApiError

Command = namedtuple("Command", ["name", "description", "arguments"])

CLIENT_WEBSITE = 'https://github.com/ihabunek/hnbex-cli'


def date_type(value):
    try:
        date = datetime.strptime(value, "%Y-%m-%d").date()
    except:
        raise ArgumentTypeError("Invalid date '{}'".format(value))

    return date


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


def print_usage():
    print_out("<green>hnbex</green> - exchange rates for HRK in your terminal")
    print_out("")
    print_out("Fetched from <yellow>HNB Exchange Rate Lookup API</yellow> by "
              "<magenta>Good Code</magenta>")
    print_out("https://hnbex.eu/")
    print_out("")
    print_out("Usage:")

    max_name_len = max(len(c.name) for c in COMMANDS)
    for command in COMMANDS:
        name = command.name.ljust(max_name_len + 2)
        print_out("  <yellow>hnbex {}</yellow> {}".format(name, command.description))

    print_out("")
    print_out("To get help for each command run:")
    print_out("  <yellow>hnbex <command> --help</yellow>")
    print_out("")
    print_out("<green>{}</green>".format(CLIENT_WEBSITE))


def get_argument_parser(name, command):
    parser = ArgumentParser(
        prog='hnbex %s' % name,
        description=command.description,
        epilog=CLIENT_WEBSITE)

    for args, kwargs in command.arguments + COMMON_ARGS:
        parser.add_argument(*args, **kwargs)

    return parser


def run_command(name, args):
    command = next((c for c in COMMANDS if c.name == name), None)

    if not command:
        print_err("Unknown command '{}'".format(name))
        sys.exit(1)

    parser = get_argument_parser(name, command)
    parsed_args = parser.parse_args(args)

    fn = commands.__dict__.get(name)

    if not fn:
        raise NotImplementedError("Command '{}' does not have an implementation.".format(name))

    return fn(**parsed_args.__dict__)


def main():
    command_name = sys.argv[1] if len(sys.argv) > 1 else None
    args = sys.argv[2:]

    if not command_name:
        return print_usage()

    try:
        run_command(command_name, args)
    except Exception as e:
        print_err(str(e))
        sys.exit(1)
