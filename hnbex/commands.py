import tempfile

from datetime import timedelta
from decimal import Decimal
from importlib.resources import files
from os.path import realpath, join, dirname
from subprocess import call

from hnbex.api import fetch_daily, fetch_range
from hnbex.output import print_out, print_err, print_table


class CommandError(Exception):
    pass


def wrap(tag, text):
    return f"<{tag}>{text}</{tag}>"


def daily(date, invert: bool, **kwargs):
    rates = fetch_daily(date)

    print_out(f"HNB exchange rates on <yellow>{date:%Y-%m-%d}</yellow>")
    print_out()

    if len(rates) == 0:
        print_out("No data found for given date")
        return

    def spread(rate):
        buy = rate.buying_rate
        sell = rate.selling_rate
        if buy > 0:
            diff = (buy - sell) / buy
            return f"{diff:.2%}"
        return ""

    data = [(
        wrap("yellow", rate.currency_code),
        _maybe_invert(rate.buying_rate, invert),
        _maybe_invert(rate.median_rate, invert),
        _maybe_invert(rate.selling_rate, invert),
        spread(rate)
    ) for rate in rates]

    headers = ["Currency", "Buying", "Median", "Selling", "Spread"]
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
    formatted = f"{diff:.2%}"

    if diff < 0:
        return f"<red>{formatted}</red>"

    if diff > 0:
        return f"<green>+{formatted}</green>"

    return f" {formatted}"


def _range_lines(rates, invert):
    prev_median = None
    diff_median = None

    for rate in rates:
        median = _maybe_invert(rate.median_rate, invert)
        diff_median = _diff(prev_median, median)

        yield(
            wrap("yellow", rate.date),
            _maybe_invert(rate.buying_rate, invert),
            _maybe_invert(rate.median_rate, invert),
            _maybe_invert(rate.selling_rate, invert),
            diff_median,
        )

        prev_median = median


def range(currency, start, end, days, invert, **kwargs):
    start_date, end_date = _range_dates(start, end, days)
    rates = fetch_range(currency, start_date, end_date)

    print_out(
        f"HNB exchange rates for <yellow>{currency}</yellow>",
        f"from <yellow>{start_date:%Y-%m-%d}</yellow>",
        f"to <yellow>{end_date:%Y-%m-%d}</yellow>\n"
    )

    if not rates:
        print_out("No data found for given date range")
        return

    headers = ['Date', 'Buying', 'Median', 'Selling', 'Diff']
    print_table(headers, _range_lines(rates, invert))


def _get_rate(date, currency):
    rates = fetch_daily(date, currency_code=currency)

    if rates:
        return rates[0]

    raise CommandError(f"Exchange rate for {currency} not found")


def convert(amount, source_currency, target_currency, date, precision, value_only, **kwargs):
    if precision < 0:
        raise CommandError("Precision must be greater than 0.")

    if source_currency != 'EUR' and target_currency != 'EUR':
        raise CommandError("Either source or target currency must be EUR.")

    if source_currency == target_currency:
        raise CommandError("Source and target currency are the same.")

    if source_currency == 'EUR':
        rate = _get_rate(date, target_currency)
        result = amount * rate.median_rate
    else:
        rate = _get_rate(date, source_currency)
        result = amount / rate.median_rate

    result = quantize(result, precision)

    if value_only:
        print_out(result)
    else:
        print_out(f"{amount} {source_currency} = <green>{result} {target_currency}</green>\n")
        print_out(
            f"Using the median rate 1 EUR =",
            f"{rate.median_rate} {rate.currency_code} defined on {rate.date}"
        )


def abspath(path):
    return join(realpath(dirname(__file__)), path)


def chart(currency, template, start, end, days, **kwargs):
    start_date, end_date = _range_dates(start, end, days)
    rates = fetch_range(currency, start_date, end_date)
    plot_data = "\n".join([f"{rate.date} {rate.median_rate}" for rate in rates])

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


def _maybe_invert(value: Decimal, invert: bool):
    return quantize(1 / value, 6) if invert else value


def quantize(decimal: Decimal, precision: int):
    exponent = Decimal(10) ** -precision
    return decimal.quantize(exponent)
