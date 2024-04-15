import json
import logging

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError
from urllib.request import urlopen

logger = logging.getLogger("hnbex")


@dataclass(frozen=True)
class ExchangeRate:
    date: date
    currency_code: str
    buying_rate: Decimal
    median_rate: Decimal
    selling_rate: Decimal


class ApiError(Exception):
    pass


def fetch_daily(date: date, currency_code: Optional[str] = None) -> List[ExchangeRate]:
    url = f"https://api.hnb.hr/tecajn-eur/v3?datum-primjene={date}"

    if currency_code:
        url += f"&valuta={currency_code}"

    return _api_get(url)


def fetch_range(currency: str, from_date: date, to_date: date) -> List[ExchangeRate]:
    # Cannot filter by `valuta=USD` or similar because that returns only one day of data, not a range
    url = f"https://api.hnb.hr/tecajn-eur/v3?datum-primjene-od={from_date}&datum-primjene-do={to_date}"
    records = _api_get(url)

    # So we need to filter manually
    return [r for r in records if r.currency_code == currency]


def _api_get(url: str) -> List[ExchangeRate]:
    logger.debug(">>> GET {}".format(url))

    try:
        with urlopen(url) as response:
            data = response.read().decode('utf-8')
            logger.debug("<<< {}".format(data))
            return [_to_rate(r) for r in json.loads(data)]
    except HTTPError as e:
        logger.error(f"<<< {e}")
        raise ApiError()


def _parse_decimal(value: str) -> Decimal:
    return Decimal(value.replace(",", "."))


def _to_rate(record: Dict[str, Any]) -> ExchangeRate:
    return ExchangeRate(
        date=date.fromisoformat(record["datum_primjene"]),
        currency_code=record["valuta"],
        buying_rate=_parse_decimal(record["kupovni_tecaj"]),
        median_rate=_parse_decimal(record["srednji_tecaj"]),
        selling_rate=_parse_decimal(record["prodajni_tecaj"]),
    )
