# python-zmanim
Python Zmanim library

This project is a port from Eliyahu Hershfeld's [KosherJava project](https://github.com/KosherJava/zmanim), with some Python niceties and other minor modifications.

## Usage

Some common examples include...

#### Zmanim calculations

```python
# Initialize a new ZmanimCalendar object, defaults to using today's date in GMT, located at Greenwich, England
from zmanim.zmanim_calendar import ZmanimCalendar
calendar = ZmanimCalendar()
calendar
#=> zmanim.zmanim_calendar.ZmanimCalendar(candle_lighting_offset=18, geo_location=zmanim.util.geo_location.GeoLocation(name='Greenwich, England', latitude=51.4772, longitude=0.0, time_zone=tzfile('/usr/share/zoneinfo/GMT'), elevation=0.0), date=datetime.datetime(2018, 8, 26, 11, 40, 29, 334774), calculator=<zmanim.util.noaa_calculator.NOAACalculator object at 0x10bbf7710>)

# Calculate the sunset for today at that location
calendar.sunset()
#=> datetime.datetime(2018, 8, 26, 18, 58, 40, 796469, tzinfo=tzfile('/usr/share/zoneinfo/GMT'))        

# Prepare a new location
from zmanim.util.geo_location import GeoLocation
location = GeoLocation('Lakewood, NJ', 40.0721087, -74.2400243, 'America/New_York', elevation=15)
location
#=> zmanim.util.geo_location.GeoLocation(name='Lakewood, NJ', latitude=40.0721087, longitude=-74.2400243, time_zone=tzfile('/usr/share/zoneinfo/America/New_York'), elevation=15.0) 

# Initialize a new ZmanimCalendar object, passing a specific location and date
from datetime import date
calendar = ZmanimCalendar(geo_location=location, date=date(2017, 12, 15))
calendar
#=> zmanim.zmanim_calendar.ZmanimCalendar(candle_lighting_offset=18, geo_location=zmanim.util.geo_location.GeoLocation(name='Lakewood, NJ', latitude=40.0721087, longitude=-74.2400243, time_zone=tzfile('/usr/share/zoneinfo/America/New_York'), elevation=15.0), date=datetime.date(2017, 12, 15), calculator=<zmanim.util.noaa_calculator.NOAACalculator object at 0x10bbf7828>)

# Calculate Sof Zman Krias Shma for that location/date per the opinion of GR"A
calendar.sof_zman_shma_gra()
#=> datetime.datetime(2017, 12, 15, 9, 32, 9, 383390, tzinfo=tzfile('/usr/share/zoneinfo/America/New_York'))
```

#### Date Calculations

```python
# Initialize a new JewishDate object with today's date
from zmanim.hebrew_calendar.jewish_date import JewishDate 
date = JewishDate()
date
#=> <zmanim.hebrew_calendar.jewish_date.JewishDate gregorian_date=datetime.date(2018, 8, 26), jewish_date=(5778, 6, 15), day_of_week=1, molad_hours=0, molad_minutes=0, molad_chalakim=0>

# Calculate the JewishDate from 25 days ago
date - 25
#=> <zmanim.hebrew_calendar.jewish_date.JewishDate gregorian_date=datetime.date(2018, 8, 1), jewish_date=(5778, 5, 20), day_of_week=4, molad_hours=0, molad_minutes=0, molad_chalakim=0>

# Initialize a new JewishCalendar object for Pesach of this Jewish calendar year
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
pesach = JewishCalendar(date.jewish_year, 1, 15)
pesach
#=> <zmanim.hebrew_calendar.jewish_calendar.JewishCalendar in_israel=False, gregorian_date=datetime.date(2018, 3, 31), jewish_date=(5778, 1, 15), day_of_week=7, molad_hours=0, molad_minutes=0, molad_chalakim=0>
pesach.significant_day()
#=> 'pesach'
pesach.is_yom_tov_assur_bemelacha()
#=> True
```

There is much more functionality included than demonstrated here.  Feel free to experiment or read the source code to learn more! 

---
## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/pinnymz/python-zmanim. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.
