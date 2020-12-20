from convertdate import julian
import pytz

from . import CalTestCase

# 1492, 10, 12
C = 2266295.5


class TestJulian(CalTestCase):
    def test_julian_legal_date(self):
        try:
            julian.to_jd(1900, 2, 29)
        except ValueError:
            self.fail('Unexpected ValueError: "julian.to_jd(1900, 2, 29)"')

        self.assertRaises(ValueError, julian.to_jd, 2014, 2, 29)
        self.assertRaises(ValueError, julian.to_jd, 2014, 3, 32)
        self.assertRaises(ValueError, julian.to_jd, 2014, 4, 31)
        self.assertRaises(ValueError, julian.to_jd, 2014, 5, -1)

    def test_reflexive_julian(self):
        self.reflexive(julian)
        self.reflexive(julian, range(113957, 1574957, 365))
        self.assertEqual(julian.from_jd(julian.to_jd(-4718, 3, 5)), (-4718, 3, 5))

    def test_from_julian(self):
        jd = 2457447.5
        self.assertEqual(jd, julian.to_jd(*julian.from_jd(jd)))
        self.assertEqual(julian.from_jd(C), (1492, 10, 12))
        self.assertEqual(julian.from_jd(2400000.5), (1858, 11, 5))
        self.assertEqual(julian.from_jd(2399830.5), (1858, 5, 19))
        self.assertEqual(julian.from_jd(0), (-4712, 1, 1))
        self.assertEqual(julian.from_jd(-1763), (-4717, 3, 5))

    def test_julian_inverse(self):
        self.reflexive(julian)

    def test_to_julian(self):
        self.assertEqual(julian.to_jd(1858, 11, 5), 2400000.5)
        self.assertEqual(julian.to_jd(1492, 10, 12), C)

    def test_month_length_julian(self):
        self.assertEqual(julian.month_length(1582, 10), 31)
        self.assertEqual(julian.month_length(1977, 2), 28)
        self.assertEqual(julian.month_length(1900, 2), 29)
        self.assertEqual(julian.month_length(1904, 2), 29)

    def test_monthcalendar_julian(self):
        self.assertEqual(julian.monthcalendar(1582, 10).pop(0).pop(1), 1)
        self.assertEqual(julian.monthcalendar(1582, 10).pop().pop(3), 31)

    def test_returntype(self):
        self.assertSequenceType(julian.from_gregorian(2020, 6, 4), int)
