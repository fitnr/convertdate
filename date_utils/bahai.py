import gregorian

EPOCH = 2394646.5
WEEKDAYS = ("Jamál", "Kamál", "Fidál", "Idál",
                  "Istijlál", "Istiqlál", "Jalál")


def to_jd(major, cycle, year, month, day):
    #//  BAHAI_TO_JD  --  Determine Julian day from Bahai date
    gy = (361 * (major - 1)) + (19 * (cycle - 1)) + \
        (year - 1) + Julianday(BAHAI_EPOCH).gregorian[0]

    if month != 20:
        m = 0
    else:
        if gregorian.leap(gy + 1):
            m = -14
        else:
            m = -15
    return (gregorian.to_jd(gy, 3, 20) + (19 * (month - 1)) + m + day)


