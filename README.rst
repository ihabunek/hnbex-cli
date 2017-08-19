HNB Exchange Rate CLI
=====================

Displays exchange rates for Croatian Kuna (HRK) from the Croatian National Bank
(HNB). Data is fetched from http://hnbex.eu/. Thanks to `Good Code
<http://goodcode.io/>`_ for providing this service.


.. image:: https://img.shields.io/badge/author-%40ihabunek-blue.svg?maxAge=3600&style=flat-square
   :target: https://mastodon.social/@ihabunek
.. image:: https://img.shields.io/github/license/ihabunek/hnbex-cli.svg?maxAge=3600&style=flat-square
   :target: https://opensource.org/licenses/GPL-3.0
.. image:: https://img.shields.io/pypi/v/hnbex-cli.svg?maxAge=3600&style=flat-square
   :target: https://pypi.python.org/pypi/hnbex-cli

Usage
-----

```
hnbex - exchange rates for HRK in your terminal

Fetched from HNB Exchange Rate Lookup API by Good Code
https://hnbex.eu/

Usage:
  hnbex daily   Show daily exchange rates for all currencies
  hnbex range   Show exchange rates for a single currency in the given date range

To get help for each command run:
  hnbex <command> --help

https://github.com/ihabunek/hnbex-cli
```

Examples
--------

```
$ hnbex daily

HNB exchange rates on 2017-08-19

Currency  Unit    Buying    Median   Selling
--------  ----  --------  --------  --------
AUD          1  4.973022  4.987986  5.002950
CAD          1  4.961973  4.976904  4.991835
CZK          1  0.282354  0.283204  0.284054
DKK          1  0.991060  0.994042  0.997024
HUF        100  2.428102  2.435408  2.442714
JPY        100  5.752434  5.769743  5.787052
NOK          1  0.789995  0.792372  0.794749
SEK          1  0.772198  0.774522  0.776846
CHF          1  6.526761  6.546400  6.566039
GBP          1  8.090919  8.115265  8.139611
USD          1  6.277699  6.296589  6.315479
EUR          1  7.370018  7.392195  7.414372
PLN          1  1.724102  1.729290  1.734478
```

```
$ hnbex range usd

HNB exchange rates for USD from 2017-07-20 to 2017-08-19

Date        Unit    Buying    Median   Selling    Diff
----------  ----  --------  --------  --------  ------
2017-07-20     1  6.410916  6.430207  6.449498
2017-07-21     1  6.420634  6.439954  6.459274  +0.15%
2017-07-22     1  6.342856  6.361942  6.381028  -1.21%
2017-07-23     1  6.342856  6.361942  6.381028   0.00%
2017-07-24     1  6.342856  6.361942  6.381028   0.00%
2017-07-25     1  6.334596  6.353657  6.372718  -0.13%
2017-07-26     1  6.331255  6.350306  6.369357  -0.05%
2017-07-27     1  6.349808  6.368915  6.388022  +0.29%
2017-07-28     1  6.300061  6.319018  6.337975  -0.78%
2017-07-29     1  6.305416  6.324389  6.343362  +0.08%
2017-07-30     1  6.305416  6.324389  6.343362   0.00%
2017-07-31     1  6.305416  6.324389  6.343362   0.00%
2017-08-01     1  6.296672  6.315619  6.334566  -0.14%
2017-08-02     1  6.248590  6.267392  6.286194  -0.76%
2017-08-03     1  6.237420  6.256189  6.274958  -0.18%
2017-08-04     1  6.231043  6.249792  6.268541  -0.10%
2017-08-05     1  6.212553  6.231247  6.249941  -0.30%
2017-08-06     1  6.212553  6.231247  6.249941   0.00%
2017-08-07     1  6.212553  6.231247  6.249941   0.00%
2017-08-08     1  6.251933  6.270745  6.289557  +0.63%
2017-08-09     1  6.243550  6.262337  6.281124  -0.13%
2017-08-10     1  6.280882  6.299781  6.318680  +0.60%
2017-08-11     1  6.296927  6.315875  6.334823  +0.26%
2017-08-12     1  6.268470  6.287332  6.306194  -0.45%
2017-08-13     1  6.268470  6.287332  6.306194   0.00%
2017-08-14     1  6.268470  6.287332  6.306194   0.00%
2017-08-15     1  6.247580  6.266379  6.285178  -0.33%
2017-08-16     1  6.247580  6.266379  6.285178   0.00%
2017-08-17     1  6.285447  6.304360  6.323273  +0.61%
2017-08-18     1  6.291993  6.310926  6.329859  +0.10%
2017-08-19     1  6.277699  6.296589  6.315479  -0.23%
```
