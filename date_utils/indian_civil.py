import gregorian

INDIAN_CIVIL_WEEKDAYS = ("ravivara", "somavara", "mangalavara", "budhavara", "brahaspativara", "sukravara", "sanivara")


def to_jd(year, month, day):
    '''Obtain Julian day for Indian Civil date'''

    gyear = year + 78
    leap = gregorian.leap(gyear)
    # // Is this a leap year ?

    # 22 - leap = 21 if leap, 22 non-leap
    start = gregorian.to_jd(gyear, 3, 22 - leap)
    if leap:
        Caitra = 31
    else:
        Caitra = 30

    if month == 1:
        jd = start + (day - 1)
    else:
        jd = start + Caitra
        m = month - 2
        m = min(m, 5)
        jd += m * 31
        if month >= 8:
            m = month - 7
            jd += m * 30

        jd += day - 1

    return jd
