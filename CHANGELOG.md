# Changelog

## [Unreleased]

### Added
- Support for operating as a read-through/write-through cache
  - `get_via` (update-on-read)
  - `set_via` (update-on-write)
- Key "namespacing" (documentation to follow)

### Changed
- pylibmc is no longer a dependency
- Default cache prefix is now just "pyappcache" and slashes are added when building raw keys
- The required API surface of caches has been reduced further

### Removed
- repr no longer defined on GenericStringKey

## 0.1 - 2020-07-15

- First version
