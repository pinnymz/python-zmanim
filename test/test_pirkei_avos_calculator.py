import unittest

from zmanim.hebrew_calendar.jewish_date import JewishDate
from zmanim.limudim.calculators.pirkei_avos import PirkeiAvos


class TestPirkeiAvosCalculator(unittest.TestCase):
    def test_simple_date(self):
        test_date = JewishDate(5778, 3, 1)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5778, 3, 5))
        self.assertEqual(limud.description(), '6')

    def test_near_end_of_cycle(self):
        test_date = JewishDate(5778, 6, 20)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5778, 6, 21))
        self.assertEqual(limud.description(), '3 - 4')

    def test_after_cycle_completes(self):
        test_date = JewishDate(5778, 6, 29)
        limud = PirkeiAvos().limud(test_date)
        self.assertIsNone(limud)

    def test_before_cycle_starts(self):
        test_date = JewishDate(5778, 1, 20)
        limud = PirkeiAvos().limud(test_date)
        self.assertIsNone(limud)

    def test_8th_day_pesach_outside_israel(self):
        test_date = JewishDate(5778, 1, 22)
        limud = PirkeiAvos().limud(test_date)
        self.assertIsNone(limud)

    def test_day_after_pesach_outside_israel(self):
        test_date = JewishDate(5778, 1, 23)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5778, 1, 29))
        self.assertEqual(limud.description(), '1')

    def test_compounding_before_cycle_end_outside_israel(self):
        test_date = JewishDate(5778, 6, 14)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.description(), '2')
        test_date = JewishDate(5778, 6, 15)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.description(), '3 - 4')

    def test_8th_day_pesach_in_israel(self):
        test_date = JewishDate(5778, 1, 22)
        limud = PirkeiAvos(in_israel=True).limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5778, 1, 22))
        self.assertEqual(limud.description(), '1')

    def test_day_after_pesach_in_israel(self):
        test_date = JewishDate(5778, 1, 23)
        limud = PirkeiAvos(in_israel=True).limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5778, 1, 29))
        self.assertEqual(limud.description(), '2')

    def test_compounding_before_cycle_end_in_israel(self):
        test_date = JewishDate(5778, 6, 21)
        limud = PirkeiAvos(in_israel=True).limud(test_date)
        self.assertEqual(limud.description(), '4')
        test_date = JewishDate(5778, 6, 22)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.description(), '5 - 6')

    def test_7_iyar_on_shabbos_outside_israel_has_blank_limud(self):
        test_date = JewishDate(5769, 3, 3)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5769, 3, 7))
        self.assertIsNone(limud.unit)

    def test_iteration_following_7_iyar_on_shabbos_outside_israel_starts_new_subcycle(self):
        test_date = JewishDate(5769, 3, 8)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5769, 3, 14))
        self.assertEqual(limud.description(), '1')

    def test_7_iyar_on_shabbos_outside_israel_compounds_last_3_weeks(self):
        test_date = JewishDate(5769, 6, 2)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.description(), '6')
        test_date = JewishDate(5769, 6, 3)
        limud = PirkeiAvos().limud(test_date)
        self.assertEqual(limud.description(), '1 - 2')

    def test_7_iyar_on_shabbos_is_israel_starts_new_subcycle(self):
        test_date = JewishDate(5769, 3, 3)
        limud = PirkeiAvos(in_israel=True).limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5769, 3, 7))
        self.assertEqual(limud.description(), '1')

    def test_iteration_following_7_iyar_on_shabbos_in_israel_starts_next_unit(self):
        test_date = JewishDate(5769, 3, 8)
        limud = PirkeiAvos(in_israel=True).limud(test_date)
        self.assertEqual(limud.end_date(), JewishDate(5769, 3, 14))
        self.assertEqual(limud.description(), '2')

    def test_7_iyar_on_shabbos_in_israel_compounds_last_2_weeks(self):
        test_date = JewishDate(5769, 6, 9)
        limud = PirkeiAvos(in_israel=True).limud(test_date)
        self.assertEqual(limud.description(), '2')
        test_date = JewishDate(5769, 6, 10)
        limud = PirkeiAvos(in_israel=True).limud(test_date)
        self.assertEqual(limud.description(), '3 - 4')
