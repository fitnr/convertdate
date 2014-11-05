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

