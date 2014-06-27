import astro

def weekday_before(weekday, jd):
    return jd - astro.jwday(jd - weekday)


def search_weekday(weekday, jd, direction, offset):
    #/*  SEARCH_WEEKDAY  --  Determine the Julian date for:
    #        weekday      Day of week desired, 0 = Sunday
    #        jd           Julian date to begin search
    #        direction    1 = next weekday, -1 = last weekday
    #        offset       Offset from jd to begin search
    #*/
    return weekday_before(weekday, jd + (direction * offset))


#//  Utility weekday functions, just wrappers for search_weekday

def nearest_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 3)


def next_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 7)


def next_or_current_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 6)


def previous_weekday(weekday, jd):
    return search_weekday(weekday, jd, -1, 1)


def previous_or_current_weekday(weekday, jd):
    return search_weekday(weekday, jd, 1, 0)


def n_weeks(weekday, jd, nthweek):
    j = 7 * nthweek

    if nthweek > 0:
        j += previous_weekday(weekday, jd)
    else:
        j += next_weekday(weekday, jd)

    return j
