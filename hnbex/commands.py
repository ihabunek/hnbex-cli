from datetime import date, timedelta

from hnbex.api import fetch_daily, fetch_range
from hnbex.output import print_out


def daily(date, **kwargs):
    rates = fetch_daily(date)

    print_out("HNB exchange rates on <red>{:%Y-%m-%d}</red>".format(date))
    print_out()
    print_out("<yellow>Currency  Unit    Buying    Median   Selling</yellow>")
    print_out("<yellow>--------  ----  --------  --------  --------</yellow>")

    for line in rates:
        print_out("<yellow>{:9}</yellow> {:4}  {:8}  {:8}  {:8}".format(
            line['currency_code'],
            line['unit_value'],
            line['buying_rate'],
            line['median_rate'],
            line['selling_rate'],
        ))


def _range_dates(start_date, end_date):
    if not end_date:
        end_date = date.today()

    if not start_date:
        start_date = end_date - timedelta(days=30)

    if start_date > end_date:
        raise Exception("start_date is greater than end_date")

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
            line['date'],
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

    title = ("HNB exchange rates for <red>{}</red> from <yellow>{:%Y-%m-%d}</yellow> to "
             "<yellow>{:%Y-%m-%d}</yellow>")

    print_out(title.format(currency, start_date, end_date))
    print_out()

    if not rates:
        print_out("No data found for given date range")
        return

    print_out("<yellow>Date        Unit    Buying    Median   Selling    Diff</yellow>")
    print_out("<yellow>----------  ----  --------  --------  --------  ------</yellow>")

    for line in _range_lines(rates):
        print_out("<yellow>{:11}</yellow> {:4}  {:8}  {:8}  {:8}  {}".format(*line))
