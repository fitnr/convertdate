import sys
from setuptools import setup

readme = open('README.rst').read()

setup(
    name="convertdate",

    version="2.0.6",

    description=("Converts between Gregorian dates and other calendar systems."
                 "Calendars included: Baha'i, French Republican, Hebrew, "
                 "Indian Civil, Islamic, ISO, Julian, Mayan and Persian."),

    long_description=readme,

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
        'Topic :: Religion',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'

    ],

    install_requires=[
        'ephem>=3.7.5.3, <3.8',
        'pytz >= 2014.10, <2016'
    ]
)
