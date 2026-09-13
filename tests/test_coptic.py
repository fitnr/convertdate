from convertdate import coptic

from . import CalTestCase


class TestGregorian(CalTestCase):
    def setUp(self):
        pass

    def test_epoch(self):
        self.assertEqual(coptic.to_jd(1, 1, 1), coptic.EPOCH)
        self.assertEqual(coptic.to_jd(1, 1, 2), coptic.EPOCH + 1)
        self.assertEqual(coptic.to_jd(2, 1, 1), coptic.EPOCH + 365.0)
        self.assertEqual(coptic.from_jd(coptic.EPOCH), (1, 1, 1))

    def test_is_leap(self):
        self.assertTrue(coptic.is_leap(1839))
        self.assertTrue(coptic.is_leap(1891))
        self.assertTrue(coptic.is_leap(1999))
        self.assertTrue(coptic.is_leap(2423))

        self.assertFalse(coptic.is_leap(1800))
        self.assertFalse(coptic.is_leap(1890))
        self.assertFalse(coptic.is_leap(1956))
        self.assertFalse(coptic.is_leap(2000))

    def test_reflexive_jd(self):
        self.assertEqual(coptic.from_jd(2431772.0), (1662, 3, 3))

        # leap year 1891
        self.assertEqual(coptic.from_jd(2515715.5), (1891, 13, 5))
        self.assertEqual(coptic.to_jd(1891, 13, 5), 2515715.5)
        self.assertEqual(coptic.from_jd(2515716.0), (1891, 13, 5))

        self.assertEqual(coptic.from_jd(2515716.5), (1891, 13, 6))
        self.assertEqual(coptic.to_jd(1891, 13, 6), 2515716.5)
        self.assertEqual(coptic.from_jd(2515717.0), (1891, 13, 6))

        self.assertEqual(coptic.from_jd(2515717.5), (1892, 1, 1))
        self.assertEqual(coptic.to_jd(1892, 1, 1), 2515717.5)
        self.assertEqual(coptic.from_jd(2515718.0), (1892, 1, 1))

        # regular year 2000 (%4=0)
        self.assertEqual(coptic.from_jd(2555528.0), (2000, 13, 4))
        self.assertEqual(coptic.from_jd(2555528.5), (2000, 13, 5))
        self.assertEqual(coptic.to_jd(2000, 13, 5), 2555528.5)
        self.assertEqual(coptic.from_jd(2555529.0), (2000, 13, 5))
        self.assertEqual(coptic.from_jd(2555529.5), (2001, 1, 1))

        # regular year 1889 (%4=1)
        self.assertEqual(coptic.from_jd(2514984.5), (1889, 13, 4))
        self.assertEqual(coptic.to_jd(1889, 13, 4), 2514984.5)
        self.assertEqual(coptic.from_jd(2514985.0), (1889, 13, 4))

        self.assertEqual(coptic.from_jd(2514985.5), (1889, 13, 5))
        self.assertEqual(coptic.to_jd(1889, 13, 5), 2514985.5)
        self.assertEqual(coptic.from_jd(2514986.0), (1889, 13, 5))

        # regular year 1886 (%4=2)
        self.assertEqual(coptic.from_jd(2513888.5), (1886, 13, 4))
        self.assertEqual(coptic.to_jd(1886, 13, 4), 2513888.5)
        self.assertEqual(coptic.from_jd(2513889.0), (1886, 13, 4))
        self.assertEqual(coptic.from_jd(2513889.5), (1886, 13, 5))
        self.assertEqual(coptic.to_jd(1886, 13, 5), 2513889.5)
        self.assertEqual(coptic.from_jd(2513890.0), (1886, 13, 5))
        self.assertEqual(coptic.from_jd(2513890.5), (1887, 1, 1))
        self.assertEqual(coptic.to_jd(1887, 1, 1), 2513890.5)
        self.assertEqual(coptic.from_jd(2513891.0), (1887, 1, 1))
