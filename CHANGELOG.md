# Changelog

## [Unreleased]

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
