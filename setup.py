from setuptools import setup

try:
    readme = open('README.rst').read()
except IOError:
    readme = open('README.md').read()

setup(
    name="convertdate",

    version="2.1.0b3",

    description=("Converts between Gregorian dates and other calendar systems. "
                 "Calendars included: Baha'i, analeptic Babylonian, "
                 "French Republican, Hebrew, Indian Civil, "
                 "Islamic, ISO, Julian, Mayan, Persian, Ordinal, "
                 "Julian Day Count, and Dublin Day Count."),

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

    package_data={
        'convertdate': ['data/*.csv'],
    },

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
        'ephem>=3.7.5.3, <3.8'
    ]
)
