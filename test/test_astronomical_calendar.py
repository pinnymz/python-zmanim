import unittest
from datetime import date

from test import test_helper
from zmanim.astronomical_calendar import AstronomicalCalendar
from zmanim.util.math_helper import MathHelper


class TestAstronomicalCalendar(unittest.TestCase):
    def test_sunrise(self):
        expected_dates = ["2017-10-17T07:09:11-04:00",
                          "2017-10-17T06:39:32+03:00",
                          "2017-10-17T07:00:25-07:00",
                          "2017-10-17T05:48:20+09:00",
                          None,
                          "2017-10-17T06:54:18+14:00"]
        expected = zip(test_helper.basic_locations(), expected_dates)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.sunrise()
            return geo, (None if result is None else result.replace(microsecond=0).isoformat())

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_sunset(self):
        expected_dates = ["2017-10-17T18:14:38-04:00",
                          "2017-10-17T18:08:46+03:00",
                          "2017-10-17T18:19:05-07:00",
                          "2017-10-17T17:04:46+09:00",
                          None,
                          "2017-10-17T19:31:07+14:00"]
        expected = zip(test_helper.basic_locations(), expected_dates)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.sunset()
            return geo, (None if result is None else result.replace(microsecond=0).isoformat())

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_sea_level_sunrise(self):
        expected_dates = ["2017-10-17T07:09:51-04:00",
                          "2017-10-17T06:43:43+03:00",
                          "2017-10-17T07:01:45-07:00",
                          "2017-10-17T05:49:21+09:00",
                          None,
                          "2017-10-17T07:00:05+14:00"]
        expected = zip(test_helper.basic_locations(), expected_dates)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.sea_level_sunrise()
            return geo, (None if result is None else result.replace(microsecond=0).isoformat())

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_sea_level_sunset(self):
        expected_dates = ["2017-10-17T18:13:58-04:00",
                          "2017-10-17T18:04:36+03:00",
                          "2017-10-17T18:17:45-07:00",
                          "2017-10-17T17:03:45+09:00",
                          None,
                          "2017-10-17T19:25:19+14:00"]
        expected = zip(test_helper.basic_locations(), expected_dates)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.sea_level_sunset()
            return geo, (None if result is None else result.replace(microsecond=0).isoformat())

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_utc_sunrise(self):
        expected_times = [11.15327065, 3.65893934, 14.00708152, 20.8057012, None, 16.90510688]
        expected = zip(test_helper.basic_locations(), expected_times)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.utc_sunrise(90)
            return geo, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_utc_sunset(self):
        expected_times = [22.24410903, 15.14635336, 1.31819979, 8.07962871, None, 5.51873532]
        expected = zip(test_helper.basic_locations(), expected_times)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.utc_sunset(90)
            return geo, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_utc_sea_level_sunrise(self):
        expected_times = [11.16434723, 3.72862262, 14.02926518, 20.82268461, None, 17.00158411]
        expected = zip(test_helper.basic_locations(), expected_times)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.utc_sea_level_sunrise(90)
            return geo, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_utc_sea_level_sunset(self):
        expected_times = [22.23304301, 15.07671429, 1.29603174, 8.06265871, None, 5.42214918]
        expected = zip(test_helper.basic_locations(), expected_times)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.utc_sea_level_sunset(90)
            return geo, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_sunrise_offset_by_degrees_for_basic_locations(self):
        expected_dates = ["2017-10-17T06:10:57-04:00",
                          "2017-10-17T05:50:43+03:00",
                          "2017-10-17T06:07:22-07:00",
                          "2017-10-17T04:53:55+09:00",
                          "2017-10-17T04:47:28-04:00",
                          "2017-10-17T06:13:13+14:00"]
        expected = zip(test_helper.basic_locations(), expected_dates)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.sunrise_offset_by_degrees(102)
            return geo, (None if result is None else result.replace(microsecond=0).isoformat())

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_sunrise_offset_by_degrees_for_arctic_timezone_extremities(self):
        calc = AstronomicalCalendar(date=date(2017, 4, 20))
        calc.geo_location = test_helper.daneborg()
        result = calc.sunrise_offset_by_degrees(94)
        self.assertEqual(result.replace(microsecond=0).isoformat(), "2017-04-19T23:54:23-02:00")

    def test_sunset_offset_by_degrees_for_basic_locations(self):
        expected_dates = ["2017-10-17T19:12:49-04:00",
                          "2017-10-17T18:57:33+03:00",
                          "2017-10-17T19:12:05-07:00",
                          "2017-10-17T17:59:08+09:00",
                          "2017-10-17T19:15:04-04:00",
                          "2017-10-17T20:12:15+14:00"]
        expected = zip(test_helper.basic_locations(), expected_dates)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.sunset_offset_by_degrees(102)
            return geo, (None if result is None else result.replace(microsecond=0).isoformat())

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_sunset_offset_by_degrees_for_arctic_timezone_extremities(self):
        calc = AstronomicalCalendar(date=date(2017, 6, 21))
        calc.geo_location = test_helper.hooper_bay()
        result = calc.sunset_offset_by_degrees(94)
        self.assertEqual(result.replace(microsecond=0).isoformat(), "2017-06-22T02:00:16-08:00")

    def test_temporal_hour(self):
        expected_lengths = [0.92239132, 0.94567431, 0.93889721, 0.93666451, None, 1.03504709]
        expected = zip(test_helper.basic_locations(), expected_lengths)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.temporal_hour()
            return geo, (None if result is None else round(result / MathHelper.HOUR_MILLIS, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)

    def test_sun_transit(self):
        expected_dates = ["2017-10-17T12:41:55-04:00",
                          "2017-10-17T12:24:09+03:00",
                          "2017-10-17T12:39:45-07:00",
                          "2017-10-17T11:26:33+09:00",
                          None,
                          "2017-10-17T13:12:42+14:00"]
        expected = zip(test_helper.basic_locations(), expected_dates)
        calc = AstronomicalCalendar(date=date(2017, 10, 17))

        def test_entry(geo):
            calc.geo_location = geo
            result = calc.sun_transit()
            return geo, (None if result is None else result.replace(microsecond=0).isoformat())

        for entry in expected:
            self.assertEqual(test_entry(entry[0]), entry)


if __name__ == '__main__':
    unittest.main()