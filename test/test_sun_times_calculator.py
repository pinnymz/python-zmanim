import unittest

from dateutil import parser

from zmanim.util.geo_location import GeoLocation
from zmanim.util.sun_times_calculator import SunTimesCalculator


class TestSunTimesCalculator(unittest.TestCase):
    def test_utc_sunrise(self):
        calc = SunTimesCalculator()
        expected = [('2017-10-17', 41.1181036, -74.0840691, 0.167, 11.16276401),
                    ('1955-02-26', 31.7962994, 35.1053185, 0.754, 4.17848602),
                    ('2017-06-21', 70.1498248, 9.1456867, 0, None)]

        def test_entry(date, lat, lng, el):
            geo = GeoLocation('Sample', lat, lng, 'America/New_York', elevation=el)
            result = calc.utc_sunrise(parser.parse(date), geo, 90, True)
            return date, lat, lng, el, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0], entry[1], entry[2], entry[3]), entry)

    def test_utc_sunset(self):
        calc = SunTimesCalculator()
        expected = [('2017-10-17', 41.1181036, -74.0840691, 0.167, 22.21747591),
                    ('1955-02-26', 31.7962994, 35.1053185, 0.754, 15.58295081),
                    ('2017-06-21', 70.1498248, 9.1456867, 0, None)]

        def test_entry(date, lat, lng, el):
            geo = GeoLocation('Sample', lat, lng, 'America/New_York', elevation=el)
            result = calc.utc_sunset(parser.parse(date), geo, 90, True)
            return date, lat, lng, el, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0], entry[1], entry[2], entry[3]), entry)


if __name__ == '__main__':
    unittest.main()