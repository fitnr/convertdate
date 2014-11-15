convertdate
===========

The convertdate package was originally developed as "[Python Date Utils](http://sourceforge.net/projects/pythondateutils)" by Phil Schwartz. It had been significantly updated and expanded.

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

The `holidays` module also provides some useful holiday-calculation, with a focus on American and Jewish holidays.

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