import gregorian
import utils

def to_jd(year, week, day):
    return to_julian(year, week, day)


def day_to_jd(year, day):
    return day_to_julian(year, day)


def to_julian(year, week, day):
    '''Return Julian day of given ISO year, week, and day'''
    return day + utils.n_weeks(0, gregorian.to_jd(year - 1, 12, 28), week)


def day_to_julian(year, day):
    '''Return Julian day of given ISO year, and day of year'''
    return (day - 1) + gregorian.to_jd(year, 1, 1)

