from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
from zmanim.util.geo_location import GeoLocation


def lakewood():
    return GeoLocation('Lakewood, NJ', 40.0721087, -74.2400243, 'America/New_York', elevation=15)


def samoa():
    return GeoLocation('Apia, Samoa', -13.8599098, -171.8031745, 'Pacific/Apia', elevation=1858)


def jerusalem():
    return GeoLocation('Jerusalem, Israel', 31.7781161, 35.233804, 'Asia/Jerusalem', elevation=740)


def los_angeles():
    return GeoLocation('Los Angeles, CA', 34.0201613, -118.6919095, 'America/Los_Angeles', elevation=71)


def tokyo():
    return GeoLocation('Tokyo, Japan', 35.6733227, 139.6403486, 'Asia/Tokyo', elevation=40)


def arctic_nunavut():
    return GeoLocation('Fort Conger, NU Canada', 81.7449398, -64.7945858, 'America/Toronto', elevation=127)


def basic_locations():
    return [lakewood(), jerusalem(), los_angeles(), tokyo(), arctic_nunavut(), samoa()]


def hooper_bay():
    return GeoLocation('Hooper Bay, Alaska', 61.520182, -166.1740437, 'America/Anchorage', elevation=8)


def daneborg():
    return GeoLocation('Daneborg, Greenland', 74.2999996, -20.2420877, 'America/Godthab', elevation=0)


def standard_monday_chaseirim():
    return 5777


def standard_monday_shelaimim():
    return 5759


def standard_tuesday_kesidran():
    return 5762


def standard_thursday_kesidran():
    return 5778


def standard_thursday_shelaimim():
    return 5754


def standard_shabbos_chaseirim():
    return 5781


def standard_shabbos_shelaimim():
    return 5770


def leap_monday_chaseirim():
    return 5749


def leap_monday_shelaimim():
    return 5776


def leap_tuesday_kesidran():
    return 5755


def leap_thursday_chaseirim():
    return 5765


def leap_thursday_shelaimim():
    return 5774


def leap_shabbos_chaseirim():
    return 5757


def leap_shabbos_shelaimim():
    return 5763


def all_days_matching(year, matcher, in_israel=False, use_modern_holidays=False):
    calendar = JewishCalendar(year, 7, 1)
    calendar.in_israel = in_israel
    calendar.use_modern_holidays = use_modern_holidays
    collection = {}
    while calendar.jewish_year == year:
        sd = matcher(calendar)
        if sd:
            if sd not in collection:
                collection[sd] = []
            collection[sd] += [f'{calendar.jewish_month}-{calendar.jewish_day}']
        calendar.forward()
    return collection


def specific_days_matching(collection, days):
    return {day: collection[day] for day in days}
