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

.. code-block::

    hnbex - exchange rates for HRK in your terminal

    Fetched from HNB Exchange Rate Lookup API by Good Code
    https://hnbex.eu/

    Usage:
      hnbex daily   Show daily exchange rates for all currencies
      hnbex range   Show exchange rates for a single currency in the given date range

    To get help for each command run:
      hnbex <command> --help

    https://github.com/ihabunek/hnbex-cli

Examples
--------

.. code-block::

    $ hnbex daily

.. image:: https://raw.githubusercontent.com/ihabunek/hnbex-cli/master/images/hnbex_daily.png

.. code-block ::

    $ hnbex range usd

.. image:: https://raw.githubusercontent.com/ihabunek/hnbex-cli/master/images/hnbex_range.png
