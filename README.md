convertdate
===========

The convertdate package was originally developed as "[Python Date Utils](http://sourceforge.net/projects/pythondateutil/)" by Phil Schwartz. It had been significantly updated and expanded.

Available calendars:

* Bahai
* French Republican
* Gregorian
* Hebrew
* Indian Civil
* Islamic
* Julian
* Mayan
* Persian
* Mayan
* Dublin day count
* Julian day count

The `holidays` module also provides some useful holiday-calculation, with a focus on North American and Jewish holidays.

Installing
-------

`pip install convertdate`

Or download the package and run `python setup.py install`.

Using
-----

````python
from convertdate import french_republican
from convertdate import hebrew

french_republican.from_gregorian(2014, 10, 31)
# (223, 2, 1, 9)

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

North American holidays are the current focus of the `holidays` module, but pull requests are welcome.

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

# Some Jewish holidays are included
holidays.rosh_hashanah(2014)
# (2014, 9, 25)

# By default, the first Gregorian day of a Jewish holiday is returned
# Use the eve option to get the evening the holiday begins
holidays.hanukkah(2014, eve=1)
# (2014, 12, 16)
````

Utils
-----

Convertdate includes some utilities for manipulating and calculating dates.

````python
from convertdate import utils

# Calculate an arbitrary day of the week
THUR = 3
APRIL = 4

# 3rd Thursday in April
utils.nth_day_of_month(3, THUR, APRIL, 2014)
# (2014, 4, 17)

utils.nth_day_of_month(5, THUR, APRIL, 2014)
# IndexError: No 5th day of month 4

# Use 0 for the first argument to get the last weekday of a month
utils.nth_day_of_month(0, THUR, APRIL, 2014)
# (2014, 4, 24)
````

Note that when calculating weekdays, convertdate uses the convention of the `calendar` and `time` modules: Monday is 0, Sunday is 6.

````python
from convertdate import gregorian

SUN = 6

day = gregorian.to_jd(2014, 4, 17)
next = utils.next_weekday(SUN, day)

gregorian.from_jd(next)
# (2014, 4, 20)
````

Other utility functions:
* nearest_weekday
* next_or_current_weekday
* previous_weekday
* previous_or_current_weekday
