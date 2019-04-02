import unittest
from datetime import date, timedelta

import test.test_helper
from zmanim.hebrew_calendar.jewish_date import JewishDate


class TestJewishDate(unittest.TestCase):
    def test_init_with_no_args(self):
        today = date.today()
        subject = JewishDate()
        self.assertEqual(subject.gregorian_date, today)
        jewish_date = subject.jewish_date
        subject.date = today
        self.assertEqual(jewish_date, subject.jewish_date)

    def test_init_with_modern_date_arg(self):
        gregorian_date = date(2017, 10, 26)
        subject = JewishDate(gregorian_date)
        self.assertEqual(subject.gregorian_date, gregorian_date)
        self.assertEqual(subject.jewish_date, (5778, 8, 6))

    def test_init_with_pregregorian_date_arg(self):
        gregorian_date = date(1550, 10, 1)
        subject = JewishDate(gregorian_date)
        self.assertEqual(subject.gregorian_date, gregorian_date)
        self.assertEqual(subject.jewish_date, (5311, 7, 11))

    def test_init_with_jewish_modern_date_args(self):
        subject = JewishDate(5778, 8, 6)
        self.assertEqual(subject.jewish_date, (5778, 8, 6))
        self.assertEqual(subject.gregorian_date, date(2017, 10, 26))

    def test_init_with_jewish_pregregorian_date_args(self):
        subject = JewishDate(5311, 7, 11)
        self.assertEqual(subject.jewish_date, (5311, 7, 11))
        self.assertEqual(subject.gregorian_date, date(1550, 10, 1))

    def test_init_with_molad_arg_before_midnight(self):
        subject = JewishDate(54700170003)  # molad for 'Elul 5778'
        self.assertEqual(subject.jewish_date, (5778, 5, 30))
        self.assertEqual(subject.gregorian_date, date(2018, 8, 11))
        self.assertEqual(subject.molad_hours, 19)
        self.assertEqual(subject.molad_minutes, 33)
        self.assertEqual(subject.molad_chalakim, 9)

    def test_init_with_molad_arg_after_midnight(self):
        subject = JewishDate(54692515673)  # molad for 'Cheshvan 5778'
        self.assertEqual(subject.jewish_date, (5778, 7, 30))
        self.assertEqual(subject.gregorian_date, date(2017, 10, 20))
        self.assertEqual(subject.molad_hours, 12)
        self.assertEqual(subject.molad_minutes, 12)
        self.assertEqual(subject.molad_chalakim, 17)

    def test_from_date(self):
        gregorian_date = date(2017, 10, 26)
        subject = JewishDate.from_date(gregorian_date)
        self.assertEqual(subject.gregorian_date, gregorian_date)
        self.assertEqual(subject.jewish_date, (5778, 8, 6))

    def test_from_jewish_date(self):
        subject = JewishDate.from_jewish_date(5778, 8, 6)
        self.assertEqual(subject.jewish_date, (5778, 8, 6))
        self.assertEqual(subject.gregorian_date, date(2017, 10, 26))

    def test_from_molad(self):
        subject = JewishDate.from_molad(54692515673)
        self.assertEqual(subject.jewish_date, (5778, 7, 30))
        self.assertEqual(subject.gregorian_date, date(2017, 10, 20))

    def test_reset_date(self):
        subject = JewishDate(date.today() - timedelta(days=3))
        subject.reset_date()
        self.assertEqual(subject.gregorian_date, date.today())

    def test_date_assignment(self):
        subject = JewishDate()
        gregorian_date = date(2017, 10, 26)
        subject.date = gregorian_date
        self.assertEqual(subject.gregorian_date, gregorian_date)
        self.assertEqual(subject.jewish_date, (5778, 8, 6))
        self.assertEqual(subject.day_of_week, 5)
        subject.date = gregorian_date + timedelta(days=2)
        self.assertEqual(subject.day_of_week, 7)

    def test_date_assignment_with_prior_molad(self):
        subject = JewishDate(54692515673)
        subject.date = date(2017, 10, 26)
        self.assertEqual(subject.molad_hours, 0)
        self.assertEqual(subject.molad_minutes, 0)
        self.assertEqual(subject.molad_chalakim, 0)

    def test_set_gregorian_date(self):
        subject = JewishDate()
        subject.set_gregorian_date(2017, 10, 26)
        self.assertEqual(subject.gregorian_date, date(2017, 10, 26))
        self.assertEqual(subject.jewish_date, (5778, 8, 6))

    def test_set_gregorian_date_with_invalid_year(self):
        subject = JewishDate()
        self.assertRaises(ValueError, subject.set_gregorian_date, -5, 11, 5)

    def test_set_gregorian_date_with_invalid_month(self):
        subject = JewishDate()
        self.assertRaises(ValueError, subject.set_gregorian_date, 2000, 13, 5)

    def test_set_gregorian_date_with_invalid_day(self):
        subject = JewishDate()
        self.assertRaises(ValueError, subject.set_gregorian_date, 2000, 11, 32)

    def test_set_gregorian_date_resets_to_max_day_in_month(self):
        subject = JewishDate()
        subject.set_gregorian_date(2000, 11, 31)
        self.assertEqual(subject.gregorian_day, 30)
        subject.set_gregorian_date(2001, 2, 29)
        self.assertEqual(subject.gregorian_day, 28)

    def test_set_jewish_date(self):
        subject = JewishDate()
        subject.set_jewish_date(5778, 8, 6)
        self.assertEqual(subject.jewish_date, (5778, 8, 6))
        self.assertEqual(subject.gregorian_date, date(2017, 10, 26))

    def test_set_jewish_date_with_invalid_year(self):
        subject = JewishDate()
        self.assertRaises(ValueError, subject.set_jewish_date, 3660, 11, 23)

    def test_set_jewish_date_with_invalid_month(self):
        subject = JewishDate()
        self.assertRaises(ValueError, subject.set_jewish_date, 5778, 14, 23)

    def test_set_jewish_date_with_invalid_day(self):
        subject = JewishDate()
        self.assertRaises(ValueError, subject.set_jewish_date, 5778, 11, 31)

    def test_set_jewish_date_resets_month_to_max_month_in_year(self):
        subject = JewishDate()
        subject.set_jewish_date(5778, 13, 5)
        self.assertEqual(subject.jewish_month, 12)

    def test_set_jewish_date_resets_day_to_max_day_in_month(self):
        subject = JewishDate()
        subject.set_jewish_date(5778, 8, 30)
        self.assertEqual(subject.jewish_day, 29)
        subject.set_jewish_date(5778, 12, 30)
        self.assertEqual(subject.jewish_day, 29)

    def test_set_jewish_date_with_prior_molad(self):
        subject = JewishDate(54692515673)
        subject.set_jewish_date(5778, 8, 15)
        self.assertEqual(subject.molad_hours, 0)
        self.assertEqual(subject.molad_minutes, 0)
        self.assertEqual(subject.molad_chalakim, 0)

    def test_set_jewish_date_passing_molad(self):
        subject = JewishDate()
        subject.set_jewish_date(5778, 8, 15, 4, 5, 6)
        self.assertEqual(subject.molad_hours, 4)
        self.assertEqual(subject.molad_minutes, 5)
        self.assertEqual(subject.molad_chalakim, 6)

    def test_forward_with_no_args(self):
        subject = JewishDate(date(2017, 10, 26))
        subject.forward()
        self.assertEqual(subject.gregorian_date, date(2017, 10, 27))
        self.assertEqual(subject.jewish_date, (5778, 8, 7))

    def test_forward_with_an_increment_in_same_month(self):
        subject = JewishDate(5778, 10, 15)
        initial_gregorian = subject.gregorian_date
        subject.forward(5)
        self.assertEqual(subject.gregorian_date, initial_gregorian + timedelta(days=5))
        self.assertEqual(subject.jewish_date, (5778, 10, 20))
        self.assertEqual(subject.day_of_week, (subject.gregorian_date.isoweekday() % 7) + 1)

    def test_forward_with_an_increment_into_next_month(self):
        subject = JewishDate(5778, 10, 28)
        initial_gregorian = subject.gregorian_date
        subject.forward(5)
        self.assertEqual(subject.gregorian_date, initial_gregorian + timedelta(days=5))
        self.assertEqual(subject.jewish_date, (5778, 11, 4))

    def test_forward_with_an_increment_into_next_year(self):
        subject = JewishDate(5778, 6, 28)
        initial_gregorian = subject.gregorian_date
        subject.forward(5)
        self.assertEqual(subject.gregorian_date, initial_gregorian + timedelta(days=5))
        self.assertEqual(subject.jewish_date, (5779, 7, 4))

    def test_forward_with_a_large_increment(self):
        subject = JewishDate(5778, 6, 28)
        initial_gregorian = subject.gregorian_date
        subject.forward(505)
        self.assertEqual(subject.gregorian_date, initial_gregorian + timedelta(days=505))
        self.assertEqual(subject.jewish_date, (5780, 10, 29))

    def test_back_with_no_args(self):
        subject = JewishDate(date(2017, 10, 26))
        subject.back()
        self.assertEqual(subject.gregorian_date, date(2017, 10, 25))
        self.assertEqual(subject.jewish_date, (5778, 8, 5))

    def test_back_with_a_decrement_in_same_month(self):
        subject = JewishDate(5778, 10, 15)
        initial_gregorian = subject.gregorian_date
        subject.back(5)
        self.assertEqual(subject.gregorian_date, initial_gregorian - timedelta(days=5))
        self.assertEqual(subject.jewish_date, (5778, 10, 10))
        self.assertEqual(subject.day_of_week, (subject.gregorian_date.isoweekday() % 7) + 1)

    def test_back_with_a_decrement_into_previous_month(self):
        subject = JewishDate(5778, 11, 4)
        initial_gregorian = subject.gregorian_date
        subject.back(5)
        self.assertEqual(subject.gregorian_date, initial_gregorian - timedelta(days=5))
        self.assertEqual(subject.jewish_date, (5778, 10, 28))

    def test_back_with_a_decrement_into_previous_year(self):
        subject = JewishDate(5779, 7, 4)
        initial_gregorian = subject.gregorian_date
        subject.back(5)
        self.assertEqual(subject.gregorian_date, initial_gregorian - timedelta(days=5))
        self.assertEqual(subject.jewish_date, (5778, 6, 28))

    def test_back_with_a_large_decrement(self):
        subject = JewishDate(5779, 7, 4)
        initial_gregorian = subject.gregorian_date
        subject.back(505)
        self.assertEqual(subject.gregorian_date, initial_gregorian - timedelta(days=505))
        self.assertEqual(subject.jewish_date, (5777, 1, 30))

    def test_addition_with_an_integer(self):
        subject = JewishDate(5778, 8, 5)
        result = subject + 5
        self.assertEqual(result.gregorian_date, subject.gregorian_date + timedelta(days=5))
        self.assertEqual(result.jewish_date, (5778, 8, 10))

    def test_addition_with_a_timedelta(self):
        subject = JewishDate(5778, 8, 5)
        result = subject + timedelta(days=5)
        self.assertEqual(result.gregorian_date, subject.gregorian_date + timedelta(days=5))
        self.assertEqual(result.jewish_date, (5778, 8, 10))

    def test_subtraction_with_an_integer(self):
        subject = JewishDate(5778, 8, 5)
        result = subject - 5
        self.assertEqual(result.gregorian_date, subject.gregorian_date - timedelta(days=5))
        self.assertEqual(result.jewish_date, (5778, 7, 30))

    def test_subtraction_with_a_timedelta(self):
        subject = JewishDate(5778, 8, 5)
        result = subject - timedelta(days=5)
        self.assertEqual(result.gregorian_date, subject.gregorian_date - timedelta(days=5))
        self.assertEqual(result.jewish_date, (5778, 7, 30))

    def test_subtraction_with_another_jewish_date(self):
        subject = JewishDate(5778, 8, 5)
        result = subject - JewishDate(5778, 7, 30)
        self.assertEqual(result, timedelta(days=5))

    def test_subtraction_with_a_gregorian_date(self):
        subject = JewishDate(5778, 8, 5)
        result = subject - date(2017, 10, 21)
        self.assertEqual(result, timedelta(days=4))

    def test_comparison_with_jewish_date(self):
        date1 = JewishDate(5778, 8, 5)
        date2 = JewishDate(5778, 9, 5)
        date3 = JewishDate(5778, 6, 5)
        date2_copy = JewishDate(5778, 9, 5)
        self.assertEqual(date2, date2_copy)
        self.assertNotEqual(date2, date1)
        self.assertGreater(date2, date1)
        self.assertGreaterEqual(date2, date1)
        self.assertGreaterEqual(date2, date2_copy)
        self.assertLess(date2, date3)
        self.assertLessEqual(date2, date3)
        self.assertLessEqual(date2, date2_copy)

    def test_comparison_with_gregorian_date(self):
        date1 = JewishDate(5778, 8, 5)
        date2 = JewishDate(5778, 9, 5)
        date3 = JewishDate(5778, 6, 5)
        date2_copy = JewishDate(5778, 9, 5)
        self.assertEqual(date2, date2_copy.gregorian_date)
        self.assertNotEqual(date2, date1.gregorian_date)
        self.assertGreater(date2, date1.gregorian_date)
        self.assertGreaterEqual(date2, date1.gregorian_date)
        self.assertGreaterEqual(date2, date2_copy.gregorian_date)
        self.assertLess(date2, date3.gregorian_date)
        self.assertLessEqual(date2, date3.gregorian_date)
        self.assertLessEqual(date2, date2_copy.gregorian_date)

    def test_gregorian_year_assignment(self):
        subject = JewishDate(date(2017, 6, 7))
        subject.gregorian_year = 2016
        self.assertEqual(subject.gregorian_date, date(2016, 6, 7))
        self.assertEqual(subject.jewish_date, (5776, 3, 1))

    def test_gregorian_month_assignment(self):
        subject = JewishDate(date(2017, 6, 7))
        subject.gregorian_month = 10
        self.assertEqual(subject.gregorian_date, date(2017, 10, 7))
        self.assertEqual(subject.jewish_date, (5778, 7, 17))

    def test_gregorian_day_assignment(self):
        subject = JewishDate(date(2017, 6, 7))
        subject.gregorian_day = 30
        self.assertEqual(subject.gregorian_date, date(2017, 6, 30))
        self.assertEqual(subject.jewish_date, (5777, 4, 6))

    def test_days_in_gregorian_year_for_standard_year(self):
        subject = JewishDate()
        self.assertEqual(subject.days_in_gregorian_year(2010), 365)

    def test_days_in_gregorian_year_for_leap_year(self):
        subject = JewishDate()
        self.assertEqual(subject.days_in_gregorian_year(2012), 366)

    def test_days_in_gregorian_year_defaults_to_current_year(self):
        subject = JewishDate()
        subject.gregorian_year = 2010
        self.assertEqual(subject.days_in_gregorian_year(), 365)
        subject.gregorian_year = 2012
        self.assertEqual(subject.days_in_gregorian_year(), 366)

    def test_days_in_gregorian_month_for_long_months(self):
        subject = JewishDate()
        result = set(map(lambda m: subject.days_in_gregorian_month(m, 2010), [1, 3, 5, 7, 8, 10, 12]))
        self.assertEqual(result, {31})

    def test_days_in_gregorian_month_for_short_months(self):
        subject = JewishDate()
        result = set(map(lambda m: subject.days_in_gregorian_month(m, 2010), [4, 6, 9, 11]))
        self.assertEqual(result, {30})

    def test_days_in_gregorian_month_for_standard_year_february(self):
        subject = JewishDate()
        self.assertEqual(subject.days_in_gregorian_month(2, 2010), 28)

    def test_days_in_gregorian_month_for_leap_year_february(self):
        subject = JewishDate()
        self.assertEqual(subject.days_in_gregorian_month(2, 2012), 29)

    def test_days_in_gregorian_month_defaults_to_current_month_and_year(self):
        subject = JewishDate(date(2013, 4, 16))
        self.assertEqual(subject.days_in_gregorian_month(), 30)
        subject.set_gregorian_date(2013, 5, 16)
        self.assertEqual(subject.days_in_gregorian_month(), 31)

    def test_is_gregorian_leap_year(self):
        subject = JewishDate()
        self.assertFalse(subject.is_gregorian_leap_year(2010))
        self.assertTrue(subject.is_gregorian_leap_year(2012))
        self.assertTrue(subject.is_gregorian_leap_year(2000))
        self.assertFalse(subject.is_gregorian_leap_year(1900))

    def test_is_gregorian_leap_year_defaults_to_current_year(self):
        subject = JewishDate()
        subject.gregorian_year = 2010
        self.assertFalse(subject.is_gregorian_leap_year())
        subject.gregorian_year = 2012
        self.assertTrue(subject.is_gregorian_leap_year())

    def test_jewish_year_assignment(self):
        subject = JewishDate(5777, 3, 13)
        subject.jewish_year = 5776
        self.assertEqual(subject.jewish_date, (5776, 3, 13))
        self.assertEqual(subject.gregorian_date, date(2016, 6, 19))

    def test_jewish_month_assignment(self):
        subject = JewishDate(5777, 3, 13)
        subject.jewish_month = 7
        self.assertEqual(subject.jewish_date, (5777, 7, 13))
        self.assertEqual(subject.gregorian_date, date(2016, 10, 15))

    def test_jewish_day_assignment(self):
        subject = JewishDate(5777, 3, 13)
        subject.jewish_day = 6
        self.assertEqual(subject.jewish_date, (5777, 3, 6))
        self.assertEqual(subject.gregorian_date, date(2017, 5, 31))

    def test_days_in_jewish_year(self):
        subject = JewishDate()
        years = [(test.test_helper.standard_monday_chaseirim(), 353),
                 (test.test_helper.standard_thursday_kesidran(), 354),
                 (test.test_helper.standard_shabbos_shelaimim(), 355),
                 (test.test_helper.leap_thursday_chaseirim(), 383),
                 (test.test_helper.leap_tuesday_kesidran(), 384),
                 (test.test_helper.leap_monday_shelaimim(), 385)]

        result = map(lambda pair: (pair[0], subject.days_in_jewish_year(pair[0])), years)
        self.assertEqual(list(result), years)

    def test_days_in_jewish_year_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertEqual(subject.days_in_jewish_year(), 355)
        subject.jewish_year = test.test_helper.leap_thursday_chaseirim()
        self.assertEqual(subject.days_in_jewish_year(), 383)

    def test_months_in_jewish_year(self):
        subject = JewishDate()
        self.assertEqual(subject.months_in_jewish_year(test.test_helper.standard_shabbos_shelaimim()), 12)
        self.assertEqual(subject.months_in_jewish_year(test.test_helper.leap_thursday_chaseirim()), 13)

    def test_months_in_jewish_year_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertEqual(subject.months_in_jewish_year(), 12)
        subject.jewish_year = test.test_helper.leap_thursday_chaseirim()
        self.assertEqual(subject.months_in_jewish_year(), 13)

    def test_sorted_months_in_jewish_year(self):
        subject = JewishDate()
        standard_months = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        leap_months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        self.assertEqual(subject.sorted_months_in_jewish_year(test.test_helper.standard_shabbos_shelaimim()), standard_months)
        self.assertEqual(subject.sorted_months_in_jewish_year(test.test_helper.leap_thursday_chaseirim()), leap_months)

    def test_sorted_months_in_jewish_year_defaults_to_current_year(self):
        subject = JewishDate()
        standard_months = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        leap_months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertEqual(subject.sorted_months_in_jewish_year(), standard_months)
        subject.jewish_year = test.test_helper.leap_thursday_chaseirim()
        self.assertEqual(subject.sorted_months_in_jewish_year(), leap_months)

    def test_sorted_days_in_jewish_year(self):
        subject = JewishDate()
        standard_shelaimim_months = [(7, 30), (8, 30), (9, 30), (10, 29), (11, 30), (12, 29),
                                     (1, 30), (2, 29), (3, 30), (4, 29), (5, 30), (6, 29)]
        leap_chaseirim_months = [(7, 30), (8, 29), (9, 29), (10, 29), (11, 30), (12, 30), (13, 29),
                                 (1, 30), (2, 29), (3, 30), (4, 29), (5, 30), (6, 29)]

        self.assertEqual(subject.sorted_days_in_jewish_year(test.test_helper.standard_shabbos_shelaimim()), standard_shelaimim_months)
        self.assertEqual(subject.sorted_days_in_jewish_year(test.test_helper.leap_thursday_chaseirim()), leap_chaseirim_months)

    def test_sorted_days_in_jewish_year_defaults_to_current_year(self):
        subject = JewishDate()
        standard_shelaimim_months = [(7, 30), (8, 30), (9, 30), (10, 29), (11, 30), (12, 29),
                                     (1, 30), (2, 29), (3, 30), (4, 29), (5, 30), (6, 29)]
        leap_chaseirim_months = [(7, 30), (8, 29), (9, 29), (10, 29), (11, 30), (12, 30), (13, 29),
                                 (1, 30), (2, 29), (3, 30), (4, 29), (5, 30), (6, 29)]

        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertEqual(subject.sorted_days_in_jewish_year(), standard_shelaimim_months)
        subject.jewish_year = test.test_helper.leap_thursday_chaseirim()
        self.assertEqual(subject.sorted_days_in_jewish_year(), leap_chaseirim_months)

    def test_days_in_jewish_month(self):
        subject = JewishDate()
        years = [(test.test_helper.standard_monday_chaseirim(), [30, 29, 30, 29, 30, 29, 30, 29, 29, 29, 30, 29]),
                 (test.test_helper.standard_thursday_kesidran(), [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]),
                 (test.test_helper.standard_shabbos_shelaimim(), [30, 29, 30, 29, 30, 29, 30, 30, 30, 29, 30, 29]),
                 (test.test_helper.leap_thursday_chaseirim(), [30, 29, 30, 29, 30, 29, 30, 29, 29, 29, 30, 30, 29]),
                 (test.test_helper.leap_tuesday_kesidran(), [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29]),
                 (test.test_helper.leap_monday_shelaimim(), [30, 29, 30, 29, 30, 29, 30, 30, 30, 29, 30, 30, 29])]

        result = map(lambda pair: (pair[0], list(map(lambda month: subject.days_in_jewish_month(month, pair[0]),
                                                     range(1, len(pair[1]) + 1)))),
                     years)
        self.assertEqual(list(result), years)

    def test_days_in_jewish_month_defaults_to_current_month_and_year(self):
        subject = JewishDate(test.test_helper.standard_shabbos_shelaimim(), 3, 1)
        self.assertEqual(subject.days_in_jewish_month(), 30)
        subject.jewish_month = 4
        self.assertEqual(subject.days_in_jewish_month(), 29)

    def test_day_number_of_jewish_year(self):
        test_dates = [((5778, 7, 1), 1),
                      ((5778, 1, 1), 178),
                      ((5778, 6, 29), 354),
                      ((5779, 13, 29), 208),
                      ((5777, 10, 1), 89)]
        subject = JewishDate()
        result = map(lambda pair: (pair[0], subject.day_number_of_jewish_year(*pair[0])), test_dates)
        self.assertEqual(list(result), test_dates)

    def test_day_number_of_jewish_year_defaults_to_current_date(self):
        subject = JewishDate(5770, 9, 1)
        self.assertEqual(subject.day_number_of_jewish_year(), 61)
        subject.jewish_month = 10
        self.assertEqual(subject.day_number_of_jewish_year(), 91)

    def test_is_jewish_leap_year(self):
        subject = JewishDate()
        self.assertFalse(subject.is_jewish_leap_year(test.test_helper.standard_shabbos_shelaimim()))
        self.assertTrue((subject.is_jewish_leap_year(test.test_helper.leap_thursday_chaseirim())))

    def test_is_jewish_leap_year_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertFalse(subject.is_jewish_leap_year())
        subject.jewish_year = test.test_helper.leap_thursday_chaseirim()
        self.assertTrue((subject.is_jewish_leap_year()))

    def test_is_cheshvan_long(self):
        years = [(test.test_helper.standard_monday_chaseirim(), False),
                 (test.test_helper.standard_thursday_kesidran(), False),
                 (test.test_helper.standard_shabbos_shelaimim(), True),
                 (test.test_helper.leap_thursday_chaseirim(), False),
                 (test.test_helper.leap_tuesday_kesidran(), False),
                 (test.test_helper.leap_monday_shelaimim(), True)]
        subject = JewishDate()
        result = map(lambda pair: (pair[0], subject.is_cheshvan_long(pair[0])), years)
        self.assertEqual(list(result), years)

    def test_is_cheshvan_long_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_monday_chaseirim()
        self.assertFalse(subject.is_cheshvan_long())
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertTrue(subject.is_cheshvan_long())

    def test_is_cheshvan_short(self):
        years = [(test.test_helper.standard_monday_chaseirim(), True),
                 (test.test_helper.standard_thursday_kesidran(), True),
                 (test.test_helper.standard_shabbos_shelaimim(), False),
                 (test.test_helper.leap_thursday_chaseirim(), True),
                 (test.test_helper.leap_tuesday_kesidran(), True),
                 (test.test_helper.leap_monday_shelaimim(), False)]
        subject = JewishDate()
        result = map(lambda pair: (pair[0], subject.is_cheshvan_short(pair[0])), years)
        self.assertEqual(list(result), years)

    def test_is_cheshvan_short_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_monday_chaseirim()
        self.assertTrue(subject.is_cheshvan_short())
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertFalse(subject.is_cheshvan_short())

    def test_is_kislev_long(self):
        years = [(test.test_helper.standard_monday_chaseirim(), False),
                 (test.test_helper.standard_thursday_kesidran(), True),
                 (test.test_helper.standard_shabbos_shelaimim(), True),
                 (test.test_helper.leap_thursday_chaseirim(), False),
                 (test.test_helper.leap_tuesday_kesidran(), True),
                 (test.test_helper.leap_monday_shelaimim(), True)]
        subject = JewishDate()
        result = map(lambda pair: (pair[0], subject.is_kislev_long(pair[0])), years)
        self.assertEqual(list(result), years)

    def test_is_kislev_long_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_monday_chaseirim()
        self.assertFalse(subject.is_kislev_long())
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertTrue(subject.is_kislev_long())

    def test_is_kislev_short(self):
        years = [(test.test_helper.standard_monday_chaseirim(), True),
                 (test.test_helper.standard_thursday_kesidran(), False),
                 (test.test_helper.standard_shabbos_shelaimim(), False),
                 (test.test_helper.leap_thursday_chaseirim(), True),
                 (test.test_helper.leap_tuesday_kesidran(), False),
                 (test.test_helper.leap_monday_shelaimim(), False)]
        subject = JewishDate()
        result = map(lambda pair: (pair[0], subject.is_kislev_short(pair[0])), years)
        self.assertEqual(list(result), years)

    def test_is_kislev_short_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_monday_chaseirim()
        self.assertTrue(subject.is_kislev_short())
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertFalse(subject.is_kislev_short())

    def test_cheshvan_kislev_kviah(self):
        years = [(test.test_helper.standard_monday_chaseirim(), JewishDate.CHESHVAN_KISLEV_KEVIAH.chaseirim),
                 (test.test_helper.standard_thursday_kesidran(), JewishDate.CHESHVAN_KISLEV_KEVIAH.kesidran),
                 (test.test_helper.standard_shabbos_shelaimim(), JewishDate.CHESHVAN_KISLEV_KEVIAH.shelaimim),
                 (test.test_helper.leap_thursday_chaseirim(), JewishDate.CHESHVAN_KISLEV_KEVIAH.chaseirim),
                 (test.test_helper.leap_tuesday_kesidran(), JewishDate.CHESHVAN_KISLEV_KEVIAH.kesidran),
                 (test.test_helper.leap_monday_shelaimim(), JewishDate.CHESHVAN_KISLEV_KEVIAH.shelaimim)]
        subject = JewishDate()
        result = map(lambda pair: (pair[0], subject.cheshvan_kislev_kviah(pair[0])), years)
        self.assertEqual(list(result), years)

    def test_cheshvan_kislev_kviah_defaults_to_current_year(self):
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_monday_chaseirim()
        self.assertEqual(subject.cheshvan_kislev_kviah(), JewishDate.CHESHVAN_KISLEV_KEVIAH.chaseirim)
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertEqual(subject.cheshvan_kislev_kviah(), JewishDate.CHESHVAN_KISLEV_KEVIAH.shelaimim)

    def test_kviah(self):
        kviah = JewishDate.CHESHVAN_KISLEV_KEVIAH
        years = [(test.test_helper.standard_monday_chaseirim(), (2, kviah.chaseirim, 3)),
                 (test.test_helper.standard_thursday_kesidran(), (5, kviah.kesidran, 7)),
                 (test.test_helper.standard_shabbos_shelaimim(), (7, kviah.shelaimim, 3)),
                 (test.test_helper.leap_thursday_chaseirim(), (5, kviah.chaseirim, 1)),
                 (test.test_helper.leap_tuesday_kesidran(), (3, kviah.kesidran, 7)),
                 (test.test_helper.leap_monday_shelaimim(), (2, kviah.shelaimim, 7))]
        subject = JewishDate()
        result = map(lambda pair: (pair[0], subject.kviah(pair[0])), years)
        self.assertEqual(list(result), years)

    def test_kviah_defaults_to_current_year(self):
        kviah = JewishDate.CHESHVAN_KISLEV_KEVIAH
        subject = JewishDate()
        subject.jewish_year = test.test_helper.standard_monday_chaseirim()
        self.assertEqual(subject.kviah(), (2, kviah.chaseirim, 3))
        subject.jewish_year = test.test_helper.standard_shabbos_shelaimim()
        self.assertEqual(subject.kviah(), (7, kviah.shelaimim, 3))

    def test_molad(self):
        subject = JewishDate()
        molad = subject.molad(5, 5778)
        self.assertEqual(molad.jewish_date, (5778, 5, 1))
        self.assertEqual((molad.molad_hours, molad.molad_minutes, molad.molad_chalakim), (6, 49, 8))

    def test_molad_defaults_to_current_month(self):
        subject = JewishDate(5778, 5, 10)
        molad = subject.molad()
        self.assertEqual(molad.jewish_date, (5778, 5, 1))
        self.assertEqual((molad.molad_hours, molad.molad_minutes, molad.molad_chalakim), (6, 49, 8))

    def test_jewish_month_from_name(self):
        subject = JewishDate()
        month_names = map(lambda m: m.name, JewishDate.MONTHS)
        result = map(lambda name: subject.jewish_month_from_name(name), month_names)
        self.assertEqual(list(result), list(range(1, 14)))

    def test_jewish_month_name(self):
        subject = JewishDate()
        self.assertEqual(subject.jewish_month_name(3), 'sivan')
        self.assertEqual(subject.jewish_month_name(8), 'cheshvan')

    def test_jewish_month_name_defaults_to_current_month(self):
        subject = JewishDate(5778, 3, 5)
        self.assertEqual(subject.jewish_month_name(), 'sivan')
        subject.jewish_month = 8
        self.assertEqual(subject.jewish_month_name(), 'cheshvan')
