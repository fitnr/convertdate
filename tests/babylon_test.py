# -*- coding: utf-8 -*-
from copy import copy
import unittest
from convertdate import dublin
from convertdate import julian
from convertdate import utils
from convertdate import babylonian as bab
from convertdate.data import babylonian_data as data
import ephem



class test_babylon_cal(unittest.TestCase):

    def test_metonic(self):
        assert bab.metonic_number(-747) == 1
        assert bab.metonic_number(-440) == 4

        assert bab.metonic_start(-500) == -500
        assert bab.metonic_start(-380) == -386

        assert bab.metonic_start(-576) == -576

        assert bab.metonic_start(1) == -6

        assert bab.metonic_number(1) == 7

        assert bab.metonic_start(-596) == -614
        assert bab.metonic_number(-596) == 19

    def test_intercal_patterns(self):
        assert bab.intercalation(1) == dict(zip(range(1, 13), data.MONTHS))

        leapyear_A = bab.intercalate(-385)
        assert len(leapyear_A) == 13
        assert leapyear_A[13] == u"Addaru II"

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

        assert data.intercalations[bab.metonic_start(-596)][bab.metonic_number(-596)] == 'U'

        assert data.intercalations[bab.metonic_start(-596)][bab.metonic_number(-596)] == 'U'

        assert len(leapyear_U) == 13

        assert leapyear_U[7] == u"Ulūlu II"


    def test_bab_ry(self):
        assert bab.regnalyear(-330) == (6, u'Alexander the Great')
        assert bab.regnalyear(-625) == (1, u'Nabopolassar')

    def test_babylon_from_jd(self):
        # print bab.from_jd(1492870.500000, 'regnal')
        assert julian.from_jd(1492870.500000) == (-626, 4, 5)
        self.assertEqual(bab.from_jd(1492870.500000, 'regnal'), ((0, u'Nabopolassar'), u"Nisānu", 1))

        self.assertEqual(bab.from_jd(1492870.500000, 'regnal'), ((0, u'Nabopolassar'), u"Nisānu", 1))

        # print bab.from_julian(-370, 3, 25, 'regnal')

        assert bab.from_julian(-330, 7, 30, 'regnal') == ((6, u'Alexander the Great'), u'Abu', 1)

    def test_babylon_from_jd_proleptic(self):
    #     assert bab.from_jd(1736116) == (3, "Addaru", 351)
    #     assert bab.from_jd(1736138) == (25, "Addaru", 351)
    #     assert bab.from_jd(1626563) == (8, "Addaru", 52)
    #     assert bab.from_jd(1494179) == (4, "Samna", None)
        pass

    def test_load_parker_dubberstein(self):
        bab.load_parker_dubberstein()
        parkerdub = bab.PARKER_DUBBERSTEIN

        assert parkerdub[-604].get('months')

    def test_metonic_cycle(self):
        dc = dublin.from_gregorian(1900, 3, 19)
        nve = ephem.next_vernal_equinox(dc)
        metonic_months = count_pattern(nve)

        assert len(metonic_months) == 19
        assert sum(metonic_months) == 235

def thing(dat):
    pve = ephem.previous_vernal_equinox(dublin.from_jd(dat))
    pnm = ephem.previous_new_moon(dublin.from_jd(dat))
    juliandate = julian.from_jd(dat)
    days_since_pve = int(dat - dublin.to_jd(pve))
    if days_since_pve > 30:
        print bab.metonic_number(juliandate[0]),
        print juliandate,
        print days_since_pve,
        print utils.floor(dat - dublin.to_jd(pnm)),
        print bab._fromjd_proleptic(dat, -data.NABONASSAR_EPOCH)

# print 'metonic number, juliandate, days since PVE, days to NNM, babdate'

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
