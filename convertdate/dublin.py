'''Convert to and from the Dublin day count'''
from .gregorian import from_jd as greg_from_jd, to_jd as greg_to_jd
from .julian import from_jd as jul_from_jd, to_jd as jul_to_jd
from . import julianday

EPOCH = 2415020  # Julian Day Count for Dublin Count 0


def to_gregorian(dc):
    return greg_from_jd(to_jd(dc))


def from_gregorian(year, month, day):
    return from_jd(greg_to_jd(year, month, day))


def to_jd(dc):
    return dc + EPOCH


def from_jd(jdc):
    return jdc - EPOCH


def from_julian(year, month, day):
    return from_jd(jul_to_jd(year, month, day))


def to_julian(dc):
    return jul_from_jd(to_jd(dc))


def to_datetime(dc):
    return julianday.to_datetime(to_jd(dc))


def from_datetime(dt):
    return from_jd(julianday.from_datetime(dt))
