convertdate
===========

The convertdate package was originally developed as "[Python Date Utils](http://sourceforge.net/projects/pythondateutils)" by Phil Schwartz. It had been significantly updated and expanded.

Available calendars:

* Babylonian
* Bahai
* French Republican
* Gregorian
* Jewish
* Indian Civil
* Islamic
* Julian
* Mayan
* Persian
* Mayan
* Dublin day count
* Julian day count

The `holidays` module also provides some useful holiday-calculation, with a focus on American and Jewish holidays.

Installing
-------

`pip install convertdate`

Or download the package and run `python setup.py install`.

Using
-----

In general, years BC are encoded with a negative sign. Giving year 0 in the incorrect context will either give an error or bad results.

Babylonian:

````python
from convertdate import babylonian

babylonian.from_gregorian(2014, 10, 31)
# (2325, u'Araḥsamnu', 7)

babylonian.from_gregorian(2014, 10, 31, plain=True)
# (2325, 'Arahsamnu', 7)

babylonian.from_julian(-326, 4, 2, era='regnal')
# ((10, u'Alexander the Great'), u'Addaru II', 14)
````

French Republican:

````python
from convertdate import french_republican

french_republican.from_gregorian(2014, 10, 31)
# (223, 2, 1, 9)
````

Jewish (aka Hebrew):

````
from convertdate import hebrew

hebrew.from_gregorian(2014, 10, 31)
# (5775, 8, 7)
# convertdate assumes you mean the middle of the day.
# Keep in mind that for some systems, the day begins at sundown
````

Before the Common Era
---------------------

For dates before the Common Era (year 1), `convertdate` uses astronomical notation: 1 BC is recorded as 0, 2 BC is -1, etc. This system always for much easier arithmatic, at the expense of ignoring custom.

Note that for dates before 4 CE, `convertdate` uses the [proleptic Julian calendar](https://en.wikipedia.org/wiki/Proleptic_Julian_calendar). The Julian Calendar was in use from 45 BC to 4 CE, but with an irregular leap year pattern.

The [proleptic Gregorian calendar](https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar) is used for dates before 1582 CE, the year of the Gregorian calendar reform.

Holidays
--------

North American holidays are the focus of the `holidays` module, but pull requests are welcome.

````python
from convertdate import holidays

# For simplicity, functions in the holidays module return a tuple
# In the format (year, month, day)

holidays.new_years(2014)
# (2014, 1, 1)

holidays.memorial_day(2014)
# (2014, 5, 26)

# USA is default
holidays.thanksgiving(2014)
# (2014, 11, 27)

# But there is a Canadian option for some holidays
holidays.thanksgiving(2014, 'canada')
# (2014, 10, 13)

# Calculate an arbitrary day of the week
thur = 3
april = 4

# 4th wednesday in april
holidays.nth_day_of_month(4, thur, april, 2014)
# (2014, 4, 24)

holidays.nth_day_of_month(5, thur, april, 2014)
# IndexError: No 5th day of month 4

# Use 0 for the first argument to get the last weekday of a month
holidays.nth_day_of_month(0, thur, april, 2014)
# (2014, 4, 24)

````
