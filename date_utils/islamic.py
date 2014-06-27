from julian import Julianday
import astro

EPOCH = 1948439.5
WEEKDAYS = ("al-'ahad", "al-'ithnayn",
            "ath-thalatha'", "al-'arb`a'",
            "al-khamis", "al-jum`a", "as-sabt")


def leap(year):
    '''LEAP_ISLAMIC  --  Is a given year a leap year in the Islamic calendar ?'''
    return (((year * 11) + 14) % 30) < 11


def to_jd(year, month, day):
    '''TO_JD  --  Determine Julian day from Islamic date'''
    return Julianday((day +
                      astro.ceil(29.5 * (month - 1)) +
                    (year - 1) * 354 +
        astro.floor((3 + (11 * year)) / 30) +
        EPOCH) - 1)
