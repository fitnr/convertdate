from utils import floor

EPOCH = 347995.5

def leap(year):
    #//  Is a given Hebrew year a leap year ?
    return (((year * 7) + 1) % 19) < 7


def year_months(year):
    '''How many months are there in a Hebrew year (12 = normal, 13 = leap)'''
    if leap(year):
        return 13
    else:
        return 12


def delay_1(year):
    '''Test for delay of start of new year and to avoid'''
    #//  Sunday, Wednesday, and Friday as start of the new year.
    months = ((235 * year) - 234) / 19
    parts = 12084 + (13753 * months)
    day = (months * 29) + parts / 25920

    if ((3 * (day + 1)) % 7) < 3:
        day += 1

    return day


def delay_2(year):
    '''Check for delay in start of new year due to length of adjacent years'''

    last = delay_1(year - 1)
    present = delay_1(year)
    next = delay_1(year + 1)

    if next - present == 356:
        return 2
    elif present - last == 382:
        return 1
    else:
        return 0


def year_days(year):
    '''How many days are in a Hebrew year ?'''
    return to_jd(year + 1, 7, 1) - to_jd(year, 7, 1)


def month_days(year, month):
    
    '''How many days are in a given month of a given year'''

    #//  First of all, dispose of fixed-length 29 day months
    if month in (2, 4, 6, 10, 13):
        return 29

    #//  If it's not a leap year, Adar has 29 days
    if month == 12 and not leap(year):
        return 29

    #//  If it's Heshvan, days depend on length of year
    if month == 8 and (year_days(year) % 10) != 5:
        return 29

    #//  Similarly, Kislev varies with the length of year
    if month == 9 and (year_days(year) % 10) == 3:
        return 29

    #//  Nope, it's a 30 day month
    return 30


def to_jd(year, month, day):
    months = year_months(year)
    jd = EPOCH + delay_1(year) + delay_2(year) + day + 1

    if month < 7:
        for mon in range(7, months + 1):
            jd += month_days(year, mon)

        for mon in range(1, month):
            jd += month_days(year, mon)
    else:
        for mon in range(7, month):
            jd += month_days(year, mon)

    return jd

def from_jd(jd):
    jd = floor(jd) + 0.5
    count = floor(((jd - EPOCH) * 98496.0) / 35975351.0)
    year = count - 1
    i = count
    while jd >= to_jd(i, 7, 1):
        i += 1
        year += 1

    if jd < to_jd(year, 1, 1):
        first = 7
    else:
        first = 1

    month = i = first
    while jd > to_jd(year, i, month_days(year, i)):
        i += 1
        month += 1

    day = int(jd - to_jd(year, month, 1)) + 1
    return (year, month, day)

