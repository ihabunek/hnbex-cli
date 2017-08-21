from datetime import date, timedelta

from hnbex.api import fetch_daily, fetch_range
from hnbex.output import print_out, print_table


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


def _range_dates(start_date, end_date):
    if not end_date:
        end_date = date.today()

    if not start_date:
        start_date = end_date - timedelta(days=30)

    if start_date > end_date:
        raise CommandError("start_date is greater than end_date")

    return start_date, end_date


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


def range(currency, end_date, start_date, **kwargs):
    start_date, end_date = _range_dates(start_date, end_date)
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
