#!/usr/local/bin/python2.1
####!/usr/bin/env python
#  holidays-cgi.py: -*- Python -*-  DESCRIPTIVE TEXT.
#  
#  Author: Phil Schwartz (phil.schwartz@users.sourceforge.net)
#  Date: Tue Jan 21 10:11:35 2003.

import cgi
import holidays
import time
from calendar import SUNDAY
from calendar import *
import sys

MONTHS = ("January", "February", "March", "April", "May", "June",
          "July", "Auguest", "September", "October", "November", "December")

    
def print_calendar(year, month, day):
    # print a calendar for M/D/Y where D is highlighted in blue.

    setfirstweekday(SUNDAY)
    month_cal = monthcalendar(year, month)

    print "<table border=1>\n"
    print "<tr><td colspan=7><font color=blue><center>%s %d</font></center></td></tr>" % (MONTHS[month-1], year)
    print "<tr><td>S</td><td>M</td><td>T</td><td>W</td><td>T</td><td>F</td><td>S</td></tr>"
    for week in month_cal:
        print "<tr>"
        for monthday in week:
            if monthday == 0:
                print "<td>&nbsp;</td>"
                continue
            if monthday == day:
                color = "blue"
            else: 
                color = "black"

            print "<td><font color=%s>%d</td>" % (color, monthday)
        print "</tr>"
    print "</table>\n"


##########################################################################################

form = cgi.FieldStorage()
print "Content-Type: text/html\n\n"
print "<html><head></head>\n"
print "<body bgcolor=white>\n"

failed = 0

try:
    year = int(form['year'].value)
except:
    failed = 1
    print "Year must be an integer<p>\n"

try:
    holiday_func = form['holiday'].value
    if not holiday_func:
        raise Exception
except:
    failed = 1
    print "You must select a holiday from the list<P>\n"

if not failed:
#    print "Holiday:", holiday_func, "<BR>\n"
#    print "Year:", year, "<BR>\n"
    print "<center>\n"
    holiday_obj = holidays.Holidays(year)
    func = eval("holiday_obj.%s" % holiday_func)
    apply(func, ())
    tm = holiday_obj.get_tuple()

#    print "tm:", tm, "<p>"
    format_str = "%A, %B %d, %Y"
    print "The holiday falls on: <font color=blue>%s</font>" % (time.strftime(format_str, tm))
    print "<p>\n"
    print_calendar(tm[0], tm[1], tm[2])
    print "</center>\n"

   

print "</body></html>"
