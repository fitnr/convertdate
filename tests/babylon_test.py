# -*- coding: utf-8 -*-
import unittest
from convertdate import dublin
from convertdate import julian
from convertdate import utils
from convertdate import babylonian as bab
from convertdate.data import babylonian_data as data
import ephem



class test_babylon_cal(unittest.TestCase):

    def test_metonic(self):
        assert bab._metonic_number(-747) == 1
        assert bab._metonic_number(-440) == 4

        assert bab._metonic_start(-500) == -500
        assert bab._metonic_start(-380) == -386

        assert bab._metonic_start(-576) == -576

        assert bab._metonic_start(1) == -6

        assert bab._metonic_number(1) == 7

    def test_intercal_patterns(self):
        assert data.intercalation(1) == dict(zip(range(1, 13), data.MONTHS))

        leapyear_A = bab.intercalate(-383)
        assert len(leapyear_A) == 13
        assert leapyear_A[13] == u"Addaru II"

        print bab.intercalate(-576)
        assert len(bab.intercalate(-576)) == 12
        assert len(bab.intercalate(-595)) == 12
        assert len(bab.intercalate(-535)) == 12

        leapyear_U = bab.intercalate(-596)
        assert bab.intercalation_pattern('U') == {
            1: u'Nis\u0101nu', 2: u'\u0100ru', 3: u'Simanu', 4: u'Dumuzu', 5: u'Abu', 6: u'Ul\u016blu',
            7: u'Ul\u016blu II', 8: u'Ti\u0161ritum', 9: u'Samna', 10: u'Kislimu', 11: u'\u1e6ceb\u0113tum',
            12: u'\u0160aba\u1e6du', 13: u'Addaru'}

        assert len(leapyear_U) == 13
        assert leapyear_U[7] == u"Ulūlu II"

    def test_bab_ry(self):
        assert bab.regnalyear(-330) == (6, u'Alexander the Great')
        assert bab.regnalyear(-625) == (1, u'Nabopolassar')

        # assert (rising.year, rising.month, rising.day) == (2014, 11, 23)

    # def test_babylon_from_jd(self):
    #     assert bab.from_jd(1736116) == (3, "Addaru", 351)
    #     assert bab.from_jd(1736138) == (25, "Addaru", 351)
    #     assert bab.from_jd(1626563) == (8, "Addaru", 52)
    #     assert bab.from_jd(1494179) == (4, "Samna", None)

def define_counts():
    y = [
        julian.to_jd(-130 - 1, 4, 16),
        julian.to_jd(-131 - 1, 4, 4),
        julian.to_jd(-132 - 1, 3, 25),
        julian.to_jd(-133 - 1, 4, 13),
        julian.to_jd(-134 - 1, 4, 3),
        julian.to_jd(-135 - 1, 4, 21),
        julian.to_jd(-136 - 1, 4, 10),
        julian.to_jd(-137 - 1, 3, 30),
        julian.to_jd(-138 - 1, 4, 18),
        julian.to_jd(-139 - 1, 4, 6),
        julian.to_jd(-140 - 1, 3, 26),
        julian.to_jd(-141 - 1, 4, 14),
        julian.to_jd(-142 - 1, 4, 4),
        julian.to_jd(-143 - 1, 4, 22),
        julian.to_jd(-144 - 1, 4, 11),
        julian.to_jd(-145 - 1, 4, 1),
        julian.to_jd(-146 - 1, 4, 20),
        julian.to_jd(-147 - 1, 4, 8),
        julian.to_jd(-148 - 1, 3, 28)
    ]

    s = [
        julian.to_jd(20 + 25, 4, 18),
        julian.to_jd(20 + 26, 4, 8),
        julian.to_jd(20 + 27, 3, 28),
        julian.to_jd(20 + 28, 4, 15),
        julian.to_jd(20 + 29, 4, 5),
        julian.to_jd(20 + 30, 3, 25),
        julian.to_jd(20 + 31, 4, 12),
        julian.to_jd(20 + 32, 4, 1),
        julian.to_jd(20 + 33, 4, 19),
        julian.to_jd(20 + 34, 4, 9),
        julian.to_jd(20 + 35, 3, 30),
        julian.to_jd(20 + 36, 4, 17),
        julian.to_jd(20 + 37, 4, 6),
        julian.to_jd(20 + 38, 3, 26),
        julian.to_jd(20 + 39, 4, 14),
        julian.to_jd(20 + 40, 4, 2),
        julian.to_jd(20 + 41, 4, 21),
        julian.to_jd(20 + 42, 4, 10),
        julian.to_jd(20 + 43, 3, 31),
        julian.to_jd(20 + 44, 4, 18),
    ]
    return y, s


def thing(dat):
    pve = ephem.previous_vernal_equinox(dat - DUBLIN_EPOCH) + DUBLIN_EPOCH
    pnm = ephem.previous_new_moon(dat - DUBLIN_EPOCH) + DUBLIN_EPOCH
    jul = julian.from_jd(dat)
    print _metonic_number(jul[0]), jul, 'days since pve:', int(dat - pve), 'days since pnm:', utils.floor(dat - pnm), _fromjd_proleptic(dat, -data.NABONASSAR_EPOCH)

print 'first day of year ... previous vernal equinox'

yearstarts, lateseleucid = define_counts()
# for date in yearstarts:
#     thing(date)

# for date in lateseleucid:
#     thing(date)

for day in range(1743763, 1743762 + 35):
    thing(day + 0.5)

#         years.append(firstday)

# years.sort()

# for firstday in years:
#     thing(firstday)
        assert len(metonic_months) == 19
        assert sum(metonic_months) == 235


def count_months_before_ve(ephemdate):
    moondate = ephemdate
    nve = ephem.next_vernal_equinox(moondate)
    count = 1

    while moondate < nve:
        try:
            moondate = _next_new_rising_babylon(moondate)
        except (ephem.NeverUpError, ephem.AlwaysUpError):
            moondate = ephem.next_new_moon(moondate)

        count += 1

    firstdaynextyear = moondate
    count = count - 1

    return count, firstdaynextyear

# (45, 4, 8) is first day of SE 356
# Has a metonic #: 13
print 'count of months'
end_of_era = ephem.date('/'.join(repr(x) for x in (45, 4, 8)) + ' 12:00:00')


def count_pattern(startingve):
    # days until ve.
    ve = copy(startingve)
    nnm = copy(startingve)

    metonic = {}

    for x in range(19):
        ve = ephem.next_vernal_equinox(ve)
        metonic[ve] = []

        while nnm < ve - 30:
            nnm = ephem.next_new_moon(nnm)
            metonic[ve].append(ephem.date(nnm))

    metonic_months = []

    for months in metonic.values():
        metonic_months.append(len(months))

    return metonic_months

if __name__ == '__main__':
    unittest.main()
