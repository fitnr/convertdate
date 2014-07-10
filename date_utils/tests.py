import unittest
import time

import utils
import bahai
import french_republican as fr
import gregorian
import hebrew
import islamic
import indian_civil
import iso
import julian
import mayan
import persian

from holidays import Holidays

"python -m unittest date_utils.tests"


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
        assert mayan.to_haab(self.c) == (16, "Sotz'")
        assert mayan.to_haab(2456282.5) == (3, "K'ank'in")

    def test_mayan_tzolkin(self):
        # tzolkin
        assert mayan.TZOLKIN_NAMES[0] == "Imix'"
        assert mayan.to_tzolkin(self.c) == (12, "B'en")
        assert mayan.to_tzolkin(2456282.5) == (4, 'Ajaw')

    def test_mayan_convenience(self):

        assert mayan.lc_to_haab(0, 0, 0, 0, 0) == (8, "Kumk'u")
        assert mayan.lc_to_tzolkin(0, 0, 0, 0, 0) == (4, "Ajaw")

        assert mayan.lc_to_tzolkin(9, 16, 12, 5, 17) == (6, "Kab'an")
        assert mayan.lc_to_haab(9, 16, 12, 5, 17) == (10, "Mol")

        assert mayan.lc_to_haab_tzolkin(9, 16, 12, 5, 17) == "6 Kab'an 10 Mol"
        

    def test_french_republican(self):
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd))

        assert fr.from_jd(gregorian.to_jd(2014, 6, 14)) == (222, 9, 3, 6)

        # 9 Thermidor II
        assert gregorian.to_jd(1794, 7, 27) == fr.to_jd(2, 11, 1, 9)

    def test_hebrew(self):
        assert self.jd == hebrew.to_jd(*hebrew.from_jd(self.jd))

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
        h = Holidays(2014, True)
        assert h.christmas == (2014, 12, 25)
        assert h.thanksgiving == (2014, 11, 27)
        assert h.easter == (2014, 4, 20)
        assert h.columbus_day == (2014, 10, 13)

if __name__ == '__main__':
    unittest.main()
