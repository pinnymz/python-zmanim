import unittest
from datetime import date

from zmanim.limudim.calculators.perek_mishnayos_yomi import PerekMishnayosYomi


class TestPerekMishnayosYomi(unittest.TestCase):
    def test_number_of_units(self):
        length = sum(PerekMishnayosYomi.PerekUnits.values())
        self.assertEqual(525, length)

    def test_simple_date(self):
        test_date = date(2017, 12, 28)
        limud = PerekMishnayosYomi().limud(test_date)
        self.assertEqual(limud.start_date(), test_date)
        self.assertEqual(limud.end_date(), test_date)
        self.assertEqual(limud.description(), 'chalah 2')

    def test_before_cycle_began(self):
        test_date = date(1947, 1, 1)
        limud = PerekMishnayosYomi().limud(test_date)
        self.assertIsNone(limud)

    def test_first_day_of_cycle(self):
        test_date = date(2019, 4, 2)
        limud = PerekMishnayosYomi().limud(test_date)
        self.assertEqual(limud.description(), 'berachos 1')

    def test_last_day_of_cycle(self):
        test_date = date(2019, 4, 1)
        limud = PerekMishnayosYomi().limud(test_date)
        self.assertEqual(limud.description(), 'uktzin 3')
