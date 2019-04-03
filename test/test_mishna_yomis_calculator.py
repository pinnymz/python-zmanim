import unittest
from datetime import date

from zmanim.limudim.calculators.mishna_yomis import MishnaYomis


class TestMishnaYomis(unittest.TestCase):
    def test_simple_date(self):
        test_date = date(2017, 12, 28)
        limud = MishnaYomis().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), 'megillah 3:4-5')

    def test_before_cycle_began(self):
        test_date = date(1947, 1, 1)
        limud = MishnaYomis().limud(test_date)
        self.assertIsNone(limud)

    def test_first_day_of_cycle(self):
        test_date = date(2016, 3, 30)
        limud = MishnaYomis().limud(test_date)
        self.assertEqual(limud.description(), 'berachos 1:1-2')

    def test_last_day_of_cycle(self):
        test_date = date(2016, 3, 29)
        limud = MishnaYomis().limud(test_date)
        self.assertEqual(limud.description(), 'uktzin 3:11-12')

    def test_span_two_masechtos(self):
        test_date = date(2016, 4, 27)
        limud = MishnaYomis().limud(test_date)
        self.assertEqual(limud.description(), 'berachos 9:5 - peah 1:1')

    def test_span_two_perakim(self):
        test_date = date(2017, 12, 23)
        limud = MishnaYomis().limud(test_date)
        self.assertEqual(limud.description(), 'megillah 1:11-2:1')
