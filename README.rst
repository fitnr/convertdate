===========
convertdate
===========

The convertdate package was originally developed as “`Python Date
Utils`_” by Phil Schwartz. It had been significantly updated and
expanded.

Available calendars:

-  Bahai
-  French Republican
-  Gregorian
-  Hebrew
-  Indian Civil
-  Islamic
-  Julian
-  Mayan
-  Persian
-  Mayan
-  ISO
-  Ordinal (day of year)
-  Dublin day count
-  Julian day count

The ``holidays`` module also provides some useful holiday-calculation,
with a focus on North American and Jewish holidays.

Installing
----------

``pip install convertdate``

Or download the package and run ``python setup.py install``.

Using
-----

::

    from convertdate import french_republican
    from convertdate import hebrew

    french_republican.from_gregorian(2014, 10, 31)
    # (223, 2, 1, 9)

    hebrew.from_gregorian(2014, 10, 31)
    # (5775, 8, 7)

Note that in some calendar systems, the day begins at sundown.
Convertdate gives the conversion for noon of the day in question.

Each module includes a monthcalendar function, which will generate a
calender-like nested list for a year and month (each list of dates runs
from Sunday to Saturday)

::

    hebrew.monthcalendar(5775, 8)
    # [
    #     [None, None, None, None, None, None, 1],
    #     [2, 3, 4, 5, 6, 7, 8],
    #     [9, 10, 11, 12, 13, 14, 15],
    #     [16, 17, 18, 19, 20, 21, 22],
    #     [23, 24, 25, 26, 27, 28, 29]
    # ]

    julian.monthcalendar(2015, 1)
    # [
    #    [None, None, None, 1, 2, 3, 4],
    #    [5, 6, 7, 8, 9, 10, 11],
    #    [12, 13, 14, 15, 16, 17, 18],
    #    [19, 20, 21, 22, 23, 24, 25],
    #    [26, 27, 28, 29, 30, 31, None]
    # ]

Special Options
---------------

French Republican
~~~~~~~~~~~~~~~~~

Leap year calculations in the French Republican calendar are a matter of dispute. By default, ``convertdate`` calculates leap years using the autumnal equinox. You can also use one of three more systematic methods proposed over the years.

* Romme, a co-creator of the calendar, proposed leap years in years divisible by four, except for years divisible by 100.
* Some concordances were drawn up in the 19th century that gave leap years every 4 years, in years that give a remainder of three when divided by four (19, 23, 27, etc...).
* Von Mädler proposed leap years in years divisible by four, except for years divisible by 128.

You can specify any of these three methods with the method keyword argument in ``french_republican`` conversion functions.

::

    from convertdate import french_republican

    # Romme's method
    french_republican.to_gregorian(20, 1, 1), method='romme')
    # (1811, 9, 23)

    # continuous method
    french_republican.to_gregorian(20, 1, 1), method='continuous')
    # (1811, 9, 24)

    # von Mädler's method
    french_republican.to_gregorian(20, 1, 1), method='madler')
    # (1811, 9, 23)

All the conversion methods correctly assign the leap years implemented while calendar was in use (3, 7, 11).

Before the Common Era
---------------------

For dates before the Common Era (year 1), ``convertdate`` uses
astronomical notation: 1 BC is recorded as 0, 2 BC is -1, etc. This
makes arithmatic much easier at the expense of ignoring custom.

Note that for dates before 4 CE, ``convertdate`` uses the `proleptic
Julian calendar`_. The Julian Calendar was in use from 45 BC, but before 4 CE the leap year leap year pattern was irregular.

The `proleptic Gregorian calendar`_ is used for dates before 1582 CE,
the year of the Gregorian calendar reform.

Holidays
--------

North American holidays are the current focus of the ``holidays``
module, but pull requests are welcome.

::

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

    # Mexican national holidays
    holidays.natalicio_benito_juarez(2016)
    # (2016, 3, 21)

    holidays.dia_revolucion(2016)
    # (2016, 11, 21)

    # Some Jewish holidays are included
    holidays.rosh_hashanah(2014)


Utils
-----

Convertdate includes some utilities for manipulating and calculating
dates.

::

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

Note that when calculating weekdays, convertdate uses the convention of the `calendar` and `time` modules: Monday is 0, Sunday is 6.

::

    from convertdate import gregorian

    SUN = 6

    day = gregorian.to_jd(2014, 4, 17)
    nextsunday = utils.next_weekday(SUN, day)

    gregorian.from_jd(nextsunday)
    # (2014, 4, 20)

Other utility functions:

- nearest_weekday
- next_or_current_weekday
- previous_weekday
- previous_or_current_weekday

.. _Python Date Utils: http://sourceforge.net/projects/pythondateutil/
.. _proleptic Julian calendar: https://en.wikipedia.org/wiki/Proleptic_Julian_calendar
.. _proleptic Gregorian calendar: https://en.wikipedia.org/wiki/Proleptic_Gregorian_calendar
