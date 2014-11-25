from setuptools import setup

setup(
    name="convertdate",

    version="2.0.3.1",

    description="Convert dates across calendar systems",

    long_description="Converts between Gregorian dates and other calendar systems. Calendars included: Baha'i, French Republican, Hebrew, Indian Civil, Islamic, Julian, Mayan and Persian.",

    author="Neil Freeman",

    license='MIT',

    author_email="contact@fakeisthenewreal.org",

    url="https://github.com/fitnr/convertdate",

    packages=[
        "convertdate",
        "convertdate.data"
    ],

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
        'ephem>=3.7.5.3'
    ]
)
