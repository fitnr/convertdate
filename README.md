
Python Date Utils
-----------------

The Python Date Utils package was developed by
Phil Schwartz.

http://sourceforge.net/projects/pythondateutils

The package contains 3 python modules:
- holidays.py
- calendar_util.py
- astro.py

astro.py is used for internal calculations by calendar_util.py and may or may not be of 
interest to you.

calendar_util.py provides functions for converting between different 
calendar systems.  The file can be executed directly to invoke it's test mode:
   $ python calendar_util.py
which will invoke most of the functions.  If you wish to import this module 
for your own application's use, it is best to look at the test code (at the end of
the file) for example usage.

holidays.py is a module that provides a class that will locate many US Federal and 
Judeo-Christian holidays in a given year.  This module depends on the calendar_util.py 
module.

There is a sample that demonstrates how to use the holidays.py module (and it's Holidays 
class) in the html_test directory.  This directory is a sample web interface to the 
holidays module.  The file html_test/cgi-bin/holidays-cgi.py is a cgi script that 
exercises the Holidays class' methods.  You can view this file for some sample usage.
You can view this simple application by visiting:
http://holidays.mailzilla.net


=======================================================================================

Install
-------

Use the script "setup.py".

  $ python setup.py build
 ($ su)
  # python setup.py install

For more information, type "python setup.py --help".


