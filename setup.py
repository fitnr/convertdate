#!/usr/bin/env python

from distutils.core import setup

setup(
    name="python_date_utils",
    version="2.0",
    description="Python Date Utils package",
    long_description="Converts between Gregorian dates and other calender systems. These calendars are included: Baha'i, French Republican, Hebrew, Indian Civil, Islamic, Julian, Mayana and Persian.",
    author="Neil Freeman and Phil Schwartz",
    license='MIT',
    author_email="contact@fakeisthenewreal.org",
    url="https://github.com/fitnr/python-date-utils",
    packages=["date_utils"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Religion',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'

    ],
    install_requires=['ephem>=3.7.5']
)
