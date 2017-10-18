#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of convertdate.
# http://github.com/fitnr/convertdate

# Licensed under the MIT license:
# http://opensource.org/licenses/MIT
# Copyright (c) 2016, fitnr <fitnr@fakeisthenewreal>
from setuptools import setup

with open('convertdate/__init__.py') as i:
    version = next(r for r in i.readlines() if '__version__' in r).split('=')[1].strip('"\' \n')

setup(
    name="convertdate",

    version=version,

    description=("Converts between Gregorian dates and other calendar systems."
                 "Calendars included: Baha'i, French Republican, Hebrew, "
                 "Indian Civil, Islamic, ISO, Julian, Mayan and Persian."),

    long_description=open('README.rst').read(),

    author="Neil Freeman",

    license='MIT',

    author_email="contact@fakeisthenewreal.org",

    url="https://github.com/fitnr/convertdate",

    packages=[
        "convertdate",
        "convertdate.data"
    ],

    test_suite='tests',

    zip_safe=True,

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Religion',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ],

    install_requires=[
        'ephem>=3.7.5.3, <3.8',
        'pytz>=2014.10, <2018'
    ]
)
