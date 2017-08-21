# -*- coding: utf-8 -*-
import sys
import re


START_CODES = {
    'red':     '\033[31m',
    'green':   '\033[32m',
    'yellow':  '\033[33m',
    'blue':    '\033[34m',
    'magenta': '\033[35m',
    'cyan':    '\033[36m',
}

END_CODE = '\033[0m'

START_PATTERN = "<(" + "|".join(START_CODES.keys()) + ")>"

END_PATTERN = "</(" + "|".join(START_CODES.keys()) + ")>"


def start_code(match):
    name = match.group(1)
    return START_CODES[name]


def colorize(text):
    text = re.sub(START_PATTERN, start_code, text)
    text = re.sub(END_PATTERN, END_CODE, text)

    return text


def strip_tags(text):
    text = re.sub(START_PATTERN, '', text)
    text = re.sub(END_PATTERN, '', text)

    return text


USE_ANSI_COLOR = "--no-color" not in sys.argv


def print_out(*args, **kwargs):
    args = [colorize(a) if USE_ANSI_COLOR else strip_tags(a) for a in args]
    print(*args, **kwargs)


def print_err(*args, **kwargs):
    args = ["<red>{}</red>".format(a) for a in args]
    args = [colorize(a) if USE_ANSI_COLOR else strip_tags(a) for a in args]
    print(*args, file=sys.stderr, **kwargs)


def print_table(headers, data, padding=2):
    """Displays data as a table"""
    data = list(data)
    widths = [len(h) for h in headers]

    def cell_len(row, idx):
        return len(strip_tags(str(row[idx])))

    def cell_pad(row, idx, width):
        return " " * (width - cell_len(row, idx)) + str(row[idx])

    for row in data:
        widths = [max(width, cell_len(row, idx)) for idx, width in enumerate(widths)]

    spacer = " " * padding
    pattern = spacer.join(["{{:>{}}}".format(w) for w in widths])
    separator = spacer.join(["-" * w for w in widths])

    print_out(pattern.format(*headers))
    print_out(separator)

    for row in data:
        row = [cell_pad(row, idx, width) for idx, width in enumerate(widths)]
        print_out(spacer.join(row))
