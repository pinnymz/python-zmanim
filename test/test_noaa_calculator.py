import unittest

from dateutil import parser

from zmanim.util.geo_location import GeoLocation
from zmanim.util.noaa_calculator import NOAACalculator


class TestNOAACalculator(unittest.TestCase):
    def test_utc_sunrise(self):
        calc = NOAACalculator()
        expected = [('2017-10-17', 41.1181036, -74.0840691, 167, 11.13543634),
                    ('2017-10-17', 34.0201613, -118.6919095, 71, 14.00708152),
                    ('1955-02-26', 31.7962994, 35.1053185, 754, 4.11885084),
                    ('2017-06-21', 70.1498248, 9.1456867, 0, None)]

        def test_entry(date, lat, lng, el):
            geo = GeoLocation('Sample', lat, lng, 'America/New_York', elevation=el)
            result = calc.utc_sunrise(parser.parse(date), geo, 90, True)
            return date, lat, lng, el, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0], entry[1], entry[2], entry[3]), entry)

    def test_utc_sunset(self):
        calc = NOAACalculator()
        expected = [('2017-10-17', 41.1181036, -74.0840691, 167, 22.24078702),
                    ('1955-02-26', 31.7962994, 35.1053185, 754, 15.64531391),
                    ('2017-06-21', 70.1498248, 9.1456867, 0, None)]

        def test_entry(date, lat, lng, el):
            geo = GeoLocation('Sample', lat, lng, 'America/New_York', elevation=el)
            result = calc.utc_sunset(parser.parse(date), geo, 90, True)
            return date, lat, lng, el, (None if result is None else round(result, 8))

        for entry in expected:
            self.assertEqual(test_entry(entry[0], entry[1], entry[2], entry[3]), entry)


if __name__ == '__main__':
    unittest.main()