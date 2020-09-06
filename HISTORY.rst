History
-------

2.2.2
-----
* Add `observed` argument to the functions for several American holidays (#30)

2.2.1
-----
* Add orthodox/eastern Easter calculations and docs
* Add module for Armenian and Sarkawag regularisation
* Bump pytz requirement

2.2.0
-----
* Repair Bahai intercalary days bug (#13, thanks @bchurchill)
* Replace pyephem, which is now in maintenance mode, with pymeeus.
* Remove shebangs and regularize licenses (thanks @fabaff)
* Convert readme to ascii (#16)

2.1.3
-----
* Bump requirements

2.1.2
-----
* Additional Jewish holidays (thanks, @ohadeytan)
* Upload source distributions to Pypi (#10)

2.1.1
-----
* Add Coptic (Alexandrian) calendar converter.
* Add explicit support for Python 3.6.

2.1.0
-----
* Change Exception thrown on illegal dates to ValueError.
* Add Comte's Positivist calendar.
* Bump requirement versions.

2.0.8
-----
* Fix Persian weekday order (thanks, @meyt)

2.0.7
-----
* Better Python 2/3 compatibility
* Improve tests
* bump pytz requirement

2.0.6
-----
* Executing holidays module returns class with current year, not '2014'.
* Expand tests for French Republican, Bahai, Persian, holidays
* Add Travis CI testing

Bug fixes:

* Fix edge case when detecting the day of fall equinox in French Republican calendar
* Fix minor methods of calculating French Republican leap years.
* Change holidays.holidays.fathers_day from a method to a property
* Add pulaski_day to holidays.holidays
* Add pytz is dependency list

2.0.5
-----
* Fix Yom Kippur error in holidays.py (issue #3)

2.0.4
-----
* Typo in name of holidays.independence_day method
* Fix major bug in ordinal.from_gregorian
* Expand and organized tests

2.0.3.1
-------
Features:

* Add `ordinal` module, for counting the day of year
* Added Mexican national holidays
* Add `monthcalendar` functions

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