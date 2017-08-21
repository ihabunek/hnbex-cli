#!/usr/bin/env python

from setuptools import setup

with open("README.rst") as readme:
    long_description = readme.read()

setup(
    name='hnbex-cli',
    version='0.4.0',
    description='CLI tool for displaying exchange rates for Croatian Kuna (HRK)',
    long_description=long_description,
    author='Ivan Habunek',
    author_email='ivan@habunek.com',
    url='https://github.com/ihabunek/hnbex/',
    keywords='hnb exchange rate currency',
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=["hnbex"],
    python_requires='>=3.3',
    entry_points={
        'console_scripts': [
            'hnbex=hnbex.console:main',
        ],
    }
)
