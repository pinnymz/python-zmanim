# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- Limudim support for: 
    - Parsha 
    - DafYomiBavli
    - DafYomiYerushalmi
    - DafHashavuaBavli
    - MishnaYomis
    - PirkeiAvos
    - TehillimMonthly
- Kviah function for JewishDate

### Fixed
- Support for python-dateutil pre-2.7.0

## [0.2.1] - 2018-01-09
### Fixed
- Reintroduced future annotations as quoted type
- Fixed bug on optimization branch for large increments/decrements

## [0.2.0] - 2018-10-04
### Added
- Backward support for Python 3.6 (removed future annotations)

## [0.1.0] - 2018-09-17
### Added
- Elevations used in shaos zmanios calculations if use_elevation property is set
- Hanetz and Shkia methods will use the appropriate calculation based on use_elevation setting
- Support Alos and Tzais offset using temporal minutes
- Various Assur Bemelacha related methods for calendar dates using JewishCalendar, 
  as well as point-in-time using ZmanimCalendar.
- Delayed candle lighting

## [0.0.2] - 2018-08-27
### Added
- README examples
- repr() content for standard classes
- This changelog :)

### Fixed
- Package license to reflect LGPLv2.1
- hebrew_calendar module now included in the package
- package includes required dependencies and python version

## [0.0.1] - 2018-08-24
### Original Alpha Release
