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

Installation
------------

Install using pip:

.. code-block::

    pip install hnbex-cli


Usage
-----

Show rates for all currencies on a given date (if not given, date defaults to today):

.. code-block::

    $ hnbex daily 2017-07-03

.. code-block::

    HNB exchange rates on 2017-07-03

    Currency  Unit    Buying    Median   Selling
    --------  ----  --------  --------  --------
    AUD          1  4.974959  4.989929  5.004899
    CAD          1  4.984697  4.999696  5.014695
    CZK          1  0.281550  0.282397  0.283244
    DKK          1  0.993132  0.996120  0.999108
    HUF        100  2.390306  2.397498  2.404690
    JPY        100  5.783341  5.800743  5.818145
    NOK          1  0.772153  0.774476  0.776799
    SEK          1  0.764812  0.767113  0.769414
    CHF          1  6.756313  6.776643  6.796973
    GBP          1  8.410575  8.435883  8.461191
    USD          1  6.474949  6.494432  6.513915
    EUR          1  7.385326  7.407549  7.429772
    PLN          1  1.748834  1.754096  1.759358


Show rates for a single currency, for range of days (if dates not given defaults to last 30 days):

.. code-block::

    hnbex range usd 2017-07-03 2017-06-20

.. code-block::

    HNB exchange rates for USD from 2017-06-20 to 2017-07-03

    Date        Unit    Buying    Median   Selling    Diff
    ----------  ----  --------  --------  --------  ------
    2017-06-20     1  6.583721  6.603532  6.623343
    2017-06-21     1  6.615151  6.635056  6.654961  +0.48%
    2017-06-22     1  6.628631  6.648577  6.668523  +0.20%
    2017-06-23     1  6.628631  6.648577  6.668523   0.00%
    2017-06-24     1  6.617416  6.637328  6.657240  -0.17%
    2017-06-25     1  6.617416  6.637328  6.657240   0.00%
    2017-06-26     1  6.617416  6.637328  6.657240   0.00%
    2017-06-27     1  6.605447  6.625323  6.645199  -0.18%
    2017-06-28     1  6.560526  6.580267  6.600008  -0.68%
    2017-06-29     1  6.500769  6.520330  6.539891  -0.91%
    2017-06-30     1  6.470754  6.490225  6.509696  -0.46%
    2017-07-01     1  6.474949  6.494432  6.513915  +0.06%
    2017-07-02     1  6.474949  6.494432  6.513915   0.00%
    2017-07-03     1  6.474949  6.494432  6.513915   0.00%


Convert between HRK and anouther currency:

.. code-block::

    $ hnbex convert 100 hrk usd

.. code-block::

    150.0 HRK = 23.82 USD

    Using the median rate 1 USD = 6.296589 HRK defined on 2017-08-21

When converting to HRK, the target currency can be ommited:

.. code-block::

    $ hnbex convert 500 jpy

.. code-block::

    500.0 JPY = 28.85 HRK

    Using the median rate 100 JPY = 5.769743 HRK defined on 2017-08-21

If ``--value-only`` or ``-v`` option is used, only the resulting value will be output.

.. code-block::

    $ hnbex convert 500 jpy

.. code-block::

    28.85

The resulting value is rounded to 2 decimal places by default but can be changed by using the ``-p`` or ``--precision`` option:

.. code-block::

    $ hnbex convert 500 jpy -p 10

.. code-block::

    28.8487150000

License
-------

Copyright © 2017 Ivan Habunek <ivan@habunek.com>

Licensed under the GPLv3: http://www.gnu.org/licenses/gpl-3.0.html
