# -*- coding: utf-8 -*-

import json

from urllib.request import urlopen
from urllib.error import HTTPError


class ApiError(Exception):
    pass


def _process_error(e):
    """
    Attempt to extract an error message from the API response.
    """

    try:
        error_msg = json.loads(e.read().decode('utf-8'))['error']
    except:
        error_msg = str(e)

    raise ApiError(error_msg)


def _api_get(url):
    try:
        with urlopen(url) as f:
            data = f.read().decode('utf-8')
            return json.loads(data)
    except HTTPError as e:
        _process_error(e)


def fetch_daily(date):
    url = 'http://hnbex.eu/api/v1/rates/daily/?date={:%Y-%m-%d}'.format(date)

    return _api_get(url)


def fetch_range(currency, from_date, to_date):
    url = 'http://hnbex.eu/api/v1/rates/{}/?from={:%Y-%m-%d}&to={:%Y-%m-%d}'.format(
        currency, from_date, to_date)

    return _api_get(url)
