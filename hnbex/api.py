# -*- coding: utf-8 -*-

import json
import logging

from urllib.request import urlopen
from urllib.error import HTTPError


logger = logging.getLogger('hnbex')


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
    logger.debug(">>> GET {}".format(url))

    try:
        with urlopen(url) as response:
            data = response.read().decode('utf-8')
            logger.debug("<<< {}".format(data))
            return json.loads(data)
    except HTTPError as e:
        logger.error("<<< {} {}".format(e.code, e.msg))
        _process_error(e)


def fetch_daily(date):
    url = 'http://hnbex.eu/api/v1/rates/daily/?date={:%Y-%m-%d}'.format(date)

    return _api_get(url)


def fetch_range(currency, from_date, to_date):
    url = 'http://hnbex.eu/api/v1/rates/{}/?from={:%Y-%m-%d}&to={:%Y-%m-%d}'.format(
        currency, from_date, to_date)

    return _api_get(url)
