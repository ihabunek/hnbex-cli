import tempfile

from datetime import timedelta
from importlib.resources import files
from os.path import realpath, join, dirname
from subprocess import call

from hnbex.api import fetch_daily, fetch_range
from hnbex.output import print_out, print_err, print_table


class CommandError(Exception):
    pass


def wrap(tag, text):
    return "<{}>{}</{}>".format(tag, text, tag)


def daily(date, **kwargs):
    rates = fetch_daily(date)

    print_out("HNB exchange rates on <yellow>{:%Y-%m-%d}</yellow>".format(date))
    print_out()

    def spread(line):
        buy = float(line['buying_rate'])
        sell = float(line['selling_rate'])
        if sell > 0:
            return "{:.2%}".format((sell - buy) / sell)
        return ""

    data = [(
        wrap('yellow', line['currency_code']),
        line['unit_value'],
        line['buying_rate'],
        line['median_rate'],
        line['selling_rate'],
        spread(line)
    ) for line in rates]

    headers = ["Currency", "Unit", "Buying", "Median", "Selling", "Spread"]
    print_table(headers, data)


def _range_dates(start, end, days):
    if not start:
        start = end - timedelta(days=days - 1)

    if start > end:
        raise CommandError("Start date cannot be greater than end date")

    return start, end


def _diff(old, new):
    if not old:
        return ""

    diff = (new - old) / old
    formatted = "{:.2%}".format(diff)

    if diff < 0:
        return "<red>{}</red>".format(formatted)

    if diff > 0:
        return "<green>+{}</green>".format(formatted)

    return " " + formatted


def _range_lines(rates):
    prev_median = None
    diff_median = None

    for line in rates:
        median = float(line['median_rate'])
        diff_median = _diff(prev_median, median)

        yield(
            wrap('yellow', line['date']),
            line['unit_value'],
            line['buying_rate'],
            line['median_rate'],
            line['selling_rate'],
            diff_median,
        )

        prev_median = float(line['median_rate'])


def range(currency, start, end, days, **kwargs):
    start_date, end_date = _range_dates(start, end, days)
    rates = fetch_range(currency, start_date, end_date)

    title = ("HNB exchange rates for <yellow>{}</yellow> from <yellow>{:%Y-%m-%d}</yellow> to "
             "<yellow>{:%Y-%m-%d}</yellow>")

    print_out(title.format(currency, start_date, end_date))
    print_out()

    if not rates:
        print_out("No data found for given date range")
        return

    headers = ['Date', 'Unit', 'Buying', 'Median', 'Selling', 'Diff']
    print_table(headers, _range_lines(rates))


def _get_median_rate(rates, currency):
    for rate in rates:
        if rate['currency_code'] == currency:
            return float(rate['median_rate']), int(rate['unit_value'])

    raise CommandError("Exchange rate for {} not found".format(currency))


def convert(amount, source_currency, target_currency, date, precision, value_only, **kwargs):
    if precision < 0:
        raise CommandError("Precision must be greater than 0.")

    if source_currency != 'HRK' and target_currency != 'HRK':
        raise CommandError("Either source or target currency must be HRK.")

    if source_currency == target_currency:
        raise CommandError("Source and target currency are the same.")

    if source_currency == 'HRK':
        rates = fetch_daily(date)
        currency = target_currency
        rate, units = _get_median_rate(rates, currency)
        result = amount / (rate / units)

    elif target_currency == 'HRK':
        rates = fetch_daily(date)
        currency = source_currency
        rate, units = _get_median_rate(rates, currency)
        result = amount * (rate / units)

    pattern = "{{:.{}f}}".format(precision)
    rounded = pattern.format(result)

    if value_only:
        print_out(rounded)
    else:
        print_out("{} {} = <green>{} {}</green>".format(
            amount, source_currency, rounded, target_currency))
        print_out("\nUsing the median rate {} {} = {} HRK defined on {}".format(
            units, currency, rate, date))


def abspath(path):
    return join(realpath(dirname(__file__)), path)


def chart(currency, template, start, end, days, **kwargs):
    start_date, end_date = _range_dates(start, end, days)
    rates = fetch_range(currency, start_date, end_date)
    plot_data = "\n".join(["{} {}".format(rate['date'], rate['median_rate'])
        for rate in rates])

    script_template = (
        files("hnbex.templates")
        .joinpath("{}.gnuplot".format(template))
        .read_text()
    )

    with tempfile.NamedTemporaryFile() as script_file:
        with tempfile.NamedTemporaryFile() as data_file:
            script = script_template.format(
                currency=currency,
                start_date=start_date,
                end_date=end_date,
                data_file=data_file.name,
            )

            script_file.write(script.encode('utf-8'))
            script_file.flush()

            data_file.write(plot_data.encode('utf-8'))
            data_file.flush()

            _plot(script_file)


def _plot(script_file):
    try:
        call(['gnuplot', '-c', script_file.name, '-p'])
    except FileNotFoundError as ex:
        print_err(ex)
        raise CommandError("Charting failed. Do you have gnuplot installed?")
