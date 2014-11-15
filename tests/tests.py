"python -m unittest convertdate.tests"

import unittest
import time

from convertdate import utils
from convertdate import bahai
from convertdate import french_republican as fr
from convertdate import gregorian
from convertdate import hebrew
from convertdate import islamic
from convertdate import indian_civil
from convertdate import iso
from convertdate import julian
from convertdate import mayan
from convertdate import persian

from convertdate import holidays


class CalTestCase(unittest.TestCase):

    def setUp(self):
        self.tm = time.localtime()
        self.gregoriandate = (self.tm[0], self.tm[1], self.tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])

        self.c_greg = (1492, 10, 21)
        self.c = gregorian.to_jd(*self.c_greg)
        self.x = gregorian.to_jd(2016, 2, 29)

    def test_utils(self):
        assert utils.amod(100, 4) == 4
        assert utils.ceil(1.2) == 2
        assert utils.jwday(self.jd) == self.tm[6]

    def test_gregorian_present(self):
        assert gregorian.to_jd(*self.gregoriandate) == self.jd
        assert gregorian.to_jd2(*self.gregoriandate) == self.jd

    def test_gregorian_1(self):
        assert self.c == 2266295.5
        assert gregorian.to_jd(2000, 1, 1) == 2451544.5

    def test_gregorian_2(self):
        assert gregorian.to_jd2(2000, 1, 1) == 2451544.5

    def test_gregorian_1_ancient(self):
        assert gregorian.to_jd(72, 6, 27) == 1747535.5

    def test_gregorian_2_ancient(self):
        assert gregorian.to_jd2(72, 6, 27) == 1747535.5

    def test_gregorian_1_ma(self):
        assert gregorian.to_jd(*self.c_greg) == 2266295.5

    def test_gregorian_2_ma(self):
        assert gregorian.to_jd2(*self.c_greg) == 2266295.5

    def test_legal_date(self):
        self.assertRaises(IndexError, gregorian.to_jd, 1900, 2, 29)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 2, 29)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 3, 32)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 4, 31)
        self.assertRaises(IndexError, gregorian.to_jd, 2014, 5, -1)

        try:
            julian.to_jd(1900, 2, 29)
        except IndexError:
            self.fail('Unexpected IndexError: "julian.to_jd(1900, 2, 29)"')

        self.assertRaises(IndexError, julian.to_jd, 2014, 2, 29)
        self.assertRaises(IndexError, julian.to_jd, 2014, 3, 32)
        self.assertRaises(IndexError, julian.to_jd, 2014, 4, 31)
        self.assertRaises(IndexError, julian.to_jd, 2014, 5, -1)


    def test_gregorian_proleptic(self):
        for y in range(int(gregorian.EPOCH), int(gregorian.EPOCH) - 10000, -100):
            assert gregorian.to_jd(*gregorian.from_jd(y)) == y - 0.5

        assert gregorian.from_jd(gregorian.to_jd(-1, 3, 1)) == (-1, 3, 1)
        assert gregorian.from_jd(gregorian.to_jd(-100, 7, 1)) == (-100, 7, 1)
        assert gregorian.from_jd(gregorian.to_jd(-500, 12, 31)) == (-500, 12, 31)
        assert gregorian.from_jd(gregorian.to_jd(-1000, 1, 1)) == (-1000, 1, 1)

    def test_mayan_reflexive(self):
        assert self.jd == mayan.to_jd(*mayan.from_jd(self.jd))

    def test_mayan_count(self):
        assert mayan.to_jd(13, 0, 0, 0, 0) == 2456282.5
        assert mayan.from_gregorian(2012, 12, 21) == (13, 0, 0, 0, 0)
        assert mayan.to_gregorian(13, 0, 0, 0, 0) == (2012, 12, 21)
        assert mayan.from_jd(self.c) == (11, 13, 12, 4, 13)

    def test_mayan_haab(self):
        # haab
        assert mayan.HAAB_MONTHS[2] == 'Zip'
        assert mayan.HAAB_MONTHS.index("Xul") == 5
        assert mayan.to_haab(self.c) == (16, "Sotz'")
        assert mayan.to_haab(2456282.5) == (3, "K'ank'in")

    def test_mayan_tzolkin(self):
        # tzolkin
        assert mayan.TZOLKIN_NAMES[0] == "Imix'"
        assert mayan.to_tzolkin(self.c) == (12, "B'en")
        assert mayan.to_tzolkin(2456282.5) == (4, 'Ajaw')
        assert mayan.to_tzolkin(2456850.5) == (13, 'Lamat')

    def test_mayan_convenience(self):

        assert mayan.lc_to_haab(0, 0, 0, 0, 0) == (8, "Kumk'u")
        assert mayan.lc_to_tzolkin(0, 0, 0, 0, 0) == (4, "Ajaw")

        assert mayan.lc_to_tzolkin(9, 16, 12, 5, 17) == (6, "Kab'an")
        assert mayan.lc_to_haab(9, 16, 12, 5, 17) == (10, "Mol")

        assert mayan.lc_to_haab_tzolkin(9, 16, 12, 5, 17) == "6 Kab'an 10 Mol"

        assert mayan.translate_haab("Wayeb'") == 'Nameless'

    def test_mayan_predictions(self):
        assert mayan.next_haab((16, "Sotz'"), self.c - 10) == self.c
        assert mayan.next_haab((0, "Pop"), 2456849.5) == 2457114.5
        assert mayan.next_tzolkin((4, 'Ajaw'), 2456182.5) == 2456282.5
        assert mayan.next_tzolkin_haab((13, "Ajaw"), (3, "Kumk'u"), 2456849.5) == 2463662.5

    def test_french_republican(self):
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd))

    def test_french_republican2(self):
        assert fr.from_gregorian(2014, 6, 14) == (222, 9, 26)

        # 9 Thermidor II
        assert gregorian.to_jd(1794, 7, 27) == fr.to_jd(2, 11, 9)

    def test_hebrew(self):
        self.assertEqual(self.jd, hebrew.to_jd(*hebrew.from_jd(self.jd)))

    def test_islamic(self):
        assert self.jd == islamic.to_jd(*islamic.from_jd(self.jd))

    def test_persian(self):
        assert self.jd == persian.to_jd(*persian.from_jd(self.jd))

    def test_indian_civil(self):
        assert self.jd == indian_civil.to_jd(*indian_civil.from_jd(self.jd))

    def test_iso(self):
        assert self.jd == iso.to_jd(*iso.from_jd(self.jd))

    def test_julian(self):
        assert self.jd == julian.to_jd(*julian.from_jd(self.jd))
        assert julian.from_jd(self.c) == (1492, 10, 12)
        assert julian.from_jd(2400000.5) == (1858, 11, 5)

    def test_bahai(self):
        assert self.jd == bahai.to_jd(*bahai.from_jd(self.jd))

    def test_holidays(self):
        h = holidays.Holidays(2014)
        assert h.christmas == (2014, 12, 25)
        assert h.thanksgiving == (2014, 11, 27)
        assert h.columbus_day == (2014, 10, 13)

    def test_thanksgiving(self):
        assert holidays.thanksgiving(2013) == (2013, 11, 28)
        assert holidays.thanksgiving(1939) == (1939, 11, 23)
        assert holidays.thanksgiving(1941) == (1941, 11, 20)

    def test_easter(self):
        easters = [
            (1994, 4, 3),
            (1995, 4, 16),
            (1996, 4, 7),
            (1997, 3, 30),
            (1998, 4, 12),
            (1999, 4, 4),
            (2000, 4, 23),
            (2001, 4, 15),
            (2002, 3, 31),
            (2003, 4, 20),
            (2004, 4, 11),
            (2005, 3, 27),
            (2006, 4, 16),
            (2007, 4, 8),
            (2008, 3, 23),
            (2009, 4, 12),
            (2010, 4, 4),
            (2011, 4, 24),
            (2012, 4, 8),
            (2013, 3, 31),
            (2014, 4, 20),
            (2015, 4, 5),
            (2016, 3, 27),
            (2017, 4, 16),
            (2018, 4, 1),
            (2019, 4, 21),
            (2020, 4, 12),
            (2021, 4, 4),
            (2022, 4, 17),
            (2023, 4, 9),
            (2024, 3, 31),
            (2025, 4, 20),
            (2026, 4, 5),
            (2027, 3, 28),
            (2028, 4, 16),
            (2029, 4, 1),
            (2030, 4, 21),
            (2031, 4, 13),
            (2032, 3, 28),
            (2033, 4, 17),
            (2034, 4, 9)
        ]
        for y, m, d in easters:
            self.assertEqual(holidays.easter(y), (y, m, d))

    def test_jewish_holidays(self):
        # http://www.chabad.org/holidays/passover/pesach_cdo/aid/671901/jewish/When-is-Passover-in-2013-2014-2015-2016-and-2017.htm
        # the date here is the start of the holiday, so the eve=1 option is used
        passovers = [
            (2013, 3, 25),
            (2014, 4, 14),
            (2015, 4, 3),
            (2016, 4, 22),
            (2017, 4, 10)
        ]
        for y, m, d in passovers:
            self.assertEqual(holidays.passover(y, eve=1), (y, m, d))

        rosh_hashanahs = [
            (2014, 9, 24),
            (2015, 9, 13),
            (2016, 10, 2),
            (2017, 9, 20),
        ]
        for y, m, d in rosh_hashanahs:
            self.assertEqual(holidays.rosh_hashanah(y, eve=1), (y, m, d))

    def test_nth_day_of_month(self):
        assert holidays.nth_day_of_month(4, 2, 4, 2014) == (2014, 4, 23)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 5, 3, 4, 2014)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 6, 2, 4, 2014)
        self.assertRaises(IndexError, holidays.nth_day_of_month, 1, 7, 4, 2014)
        assert holidays.nth_day_of_month(4, 3, 11, 2014) == (2014, 11, 27)
        assert holidays.nth_day_of_month(0, 3, 11, 2014) == (2014, 11, 27)

if __name__ == '__main__':
    unittest.main()
