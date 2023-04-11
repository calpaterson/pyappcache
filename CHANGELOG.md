# Changelog

## [Unreleased]
### Added

- Added a new serialiser which uses Parquet instead of pickle for Pandas
  dataframes: `DataFrameAwareSerialiser`.

### Changed

- Caches now work on buffers internally, rather than strs
  - This is a breaking change for compressors and serialisers
  - This seems to work much better for larger values (eg dataframes, csv files,
    etc)
- SqliteCache will now use [incremental blob
  I/O](https://www.sqlite.org/c3ref/blob.html) where possible (eg Python 3.11+)

### Removed

## 0.9.1

### Added

- `prefix` can be passed as an arg to `Cache.__init__`
- Support up to Python 3.11

### Changed

- Added a better repr for `SimpleStringKey`
- Fixed two issues in sqlite where expiry and eviction were not correct

### Removed

- Support for Python 3.6

## 0.9 - 2021-03-01

### Added

- Improved documentation greatly (and put it on RTD)
- GPLv3 license

### Changed

- Change the Key classes, a breaking change

### Removed

## 0.2 - 2021-01-14

### Added
- Support for operating as a read-through/write-through cache
  - `get_via` (update-on-read)
  - `set_via` (update-on-write)
- Key "namespacing" (documentation to follow)

### Changed
- pylibmc and redis are now optional dependencies
  - eg install `pyappcache[memcache]` or `pyappcache[redis]` to require them
- Default cache prefix is now just "pyappcache" and slashes are added when building raw keys
- The required API surface of caches has been reduced further
- MemcacheCache will retry exactly once when pylibmc raises a ConnectionError
  - in order to be robust against memcache restarts

### Removed
- repr no longer defined on GenericStringKey

## 0.1 - 2020-07-15

- First version
