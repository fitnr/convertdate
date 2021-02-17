# -*- coding: utf-8 -*-
from convertdate import gregorian, persian

from . import CalTestCase

# fmt: off
JDS = (
    2130575, 2131306, 2132036, 2132767, 2133497, 2134228, 2134958, 2135689,
    2136419, 2137150, 2137880, 2138611, 2139341, 2140072, 2140802, 2141533,
    2142263, 2142994, 2143724, 2144455, 2145185, 2145916, 2146646, 2147377,
    2148107, 2148838, 2149568, 2150299, 2151029, 2151759, 2152490, 2153220,
    2153951, 2154681, 2155412, 2156142, 2156873, 2157603, 2158334, 2159064,
    2159795, 2160525, 2161256, 2161986, 2162717, 2163447, 2164178, 2164908,
    2165639, 2166369
)
# fmt: on


class testPersian(CalTestCase):
    def setUp(self):
        self.gdate = 2021, 2, 5
        self.jd = gregorian.to_jd(*self.gdate)
        self.jdcs = range(2159677, 2488395, 2000)

    def test_equinox_jd(self):
        data = [
            (1000, 2086381),
            (1100, 2122905),
            (1199, 2159064),
            (1200, 2159430),
            (1201, 2159795),
            (1300, 2195954),
            (1400, 2232478),
            (1500, 2269002),
            (1600, 2305527),
            (1700, 2342051),
            (1800, 2378575),
            (1900, 2415099),
            (2000, 2451623),
        ]
        for gyear, jd in data:
            with self.subTest(y=gyear, jd=jd):
                self.assertEqual(persian.equinox_jd(gyear), jd)

        self.assertAlmostEqual(persian.equinox_jd(1620), 2312831, places=0)
        self.assertAlmostEqual(persian.equinox_jd(2021), 2459294, places=0)

    def test_inverse(self):
        self.assertEqual(self.jd, persian.to_jd(*persian.from_jd(self.jd)))

    def test_reflexive(self):
        self.reflexive(persian)

    def test_reverse_reflexive(self):
        date = 579, 9, 2
        self.assertEqual(persian.from_jd(persian.to_jd(*date)), date, 'from_jd(to_jd(*x)) == x')

    def test_to_jd_579(self):
        date = 579, 9, 2
        self.assertEqual(persian.to_jd(*date), 2159677.5)

    def test_from_jd_579(self):
        date = 579, 9, 2
        self.assertEqual(persian.from_jd(2159677.5), date)

    def test_leap(self):
        self.assertEqual(persian.leap(-101), False)

    def test_leapconvert(self):
        jd = 2121444.5
        self.assertSequenceEqual(persian.from_jd(jd), (475, 1, 1))
        self.assertSequenceEqual(persian.from_jd(jd - 2), (474, 12, 28))
        self.assertSequenceEqual(persian.from_jd(jd - 1), (474, 12, 29))
        jd = 2121809.5
        self.assertSequenceEqual(persian.from_jd(jd), (475, 12, 30))
        self.assertSequenceEqual(persian.from_jd(jd + 1), (476, 1, 1))

    def test_newyears(self):
        years = (1, 750, 625, 600, 580, 1000, 1400)
        jds = (1948320, 2221886, 2176231, 2167100, 2159795, 2313197, 2459294)

        for y, jd in zip(years, jds):
            jd = jd + 0.5
            with self.subTest(y=y, jd=jd):
                self.assertEqual(persian.to_jd(y, 1, 1), jd)
            with self.subTest(jd=jd, y=y):
                self.assertEqual(persian.from_jd(jd), (y, 1, 1))

    def test_examples(self):
        pairs = zip(range(500, 600, 2), JDS)

        for y, jd in pairs:
            jd = jd + 0.5
            with self.subTest(y=y, jd=jd):
                self.assertEqual(persian.to_jd(y, 1, 1), jd)
            with self.subTest(jd=jd, y=y):
                self.assertEqual(persian.from_jd(jd), (y, 1, 1))

        self.assertEqual(persian.to_jd(2021, 3, 21), 2686191.5)
        self.assertEqual(persian.to_jd(2021, 3, 20), 2686190.5)

    def test_month_length_persian(self):
        self.assertEqual(persian.month_length(1354, 12), 30)
        self.assertEqual(persian.month_length(1355, 12), 29)

    def test_monthcalendar_persian(self):
        self.assertEqual(persian.monthcalendar(1393, 8).pop(0).pop(4), 1)
        self.assertEqual(persian.monthcalendar(1393, 8).pop().pop(0), 25)
