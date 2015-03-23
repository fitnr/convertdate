History
-------

2.0.4
-----

Bug fixes:
* Typo in name of holidays.independence_day method
* Fix major bug in ordinal.from_gregorian

Other changes:
* Expand and organized tests

2.0.3.1
-------

Features:

- Add `ordinal` module, for counting the day of year
- Added Mexican national holidays
- Add `monthcalendar` functions

Other changes:
* Simplified logic in `ISO` module

2.0.3
-----

Features:

- Add list of day names and `day_name` function to French Republican converter
- Add multiple conversion methods to the French Republican calendar
- Add Dublin day count and Julian day count converters
- Add month names to Bahai and Hebrew calendars.

Other changes:

- Clarify that weekdays run Monday=0 to Sunday=6 (#2)
- Change Julian converter to use astronomical notation (0 = 1 BCE, -1 = 1 BCE)
- Expanded tests

2.0.2
-----

Features:

* Add support for Python 3 (#1)