import unittest
import time

import astro
import bahai
import french_republican as fr
import gregorian
import hebrew
import indian_civil
import iso
import julian
import mayan
import persian

"python -m unittest date_utils.tests"

class CalTestCase(unittest.TestCase):

    def setUp(self):
        tm = time.localtime()
        self.gregoriandate = (tm[0], tm[1], tm[2])

        self.jd = gregorian.to_jd(self.gregoriandate[0], self.gregoriandate[1], self.gregoriandate[2])        

        self.c = gregorian.to_jd(1492, 10, 12)
        self.x = gregorian.to_jd(2016, 2, 29)

    def test_jd(self):
        assert self.c == 2266295.5
        assert self.x == 2457447.5  

    def test_gregorian(self):
        assert self.gregoriandate == gregorian.from_jd(self.jd)
        assert gregorian.to_jd(2000, 1, 1) == 2451544.5

    def test_mayan_count(self):
        assert self.jd == mayan.to_jd(*mayan.from_jd(self.jd))
        assert mayan.to_jd(13, 0, 0, 0, 0) == 2456282.5

        assert mayan.from_gregorian(2012, 12, 21) == (13, 0, 0, 0, 0)
        assert mayan.to_gregorian(13, 0, 0, 0, 0) == (2012, 12, 21)

        assert mayan.from_jd(self.c) == (11, 13, 12, 4, 13)

    def test_mayan_haab(self):
        # haab
        assert mayan.to_haab(2456282.5) == (3, "K'ank'in")
        assert mayan.to_haab(self.c) == (12, "B'en")

    def test_mayan_tzolkin(self):
        # tzolkin
        assert mayan.to_tzolkin(2456282.5) == (4, 'Ajaw')
        assert mayan.to_tzolkin(self.c) == (16, "Sotz'")

    def test_french_republican(self):
        assert self.jd == fr.to_jd(*fr.from_jd(self.jd))

        assert fr.from_jd(gregorian.to_jd(2014, 6, 14)) == (222, 10, 3, 8)

        # 9 Thermidor II
        assert gregorian.to_jd(1794, 7, 27) == fr.to_jd(2, 11, 1, 9)

    def test_hebrew(self):
        pass

    def test_islamic(self):
        pass

    def test_persian(self):
        pass

    def test_indian_civil(self):
        pass

    def test_iso(self):
        pass

    def test_julian(self):
        pass

    def test_bahai(self):
        pass


if __name__ == '__main__':
    unittest.main()
