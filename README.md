convertdate
===========

The convertdate package was originally developed as '[Python Date Utils](http://sourceforge.net/projects/pythondateutils)' by Phil Schwartz. 

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

`python setup.py install`


Using
---
````python

from convertdate import french_republican

french_republican.from_gregorian(2014, 10, 31)
#

````