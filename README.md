# pyappcache

Pyappcache is a library to make it easier to use application-level caching in Python.

- Allows putting arbitrary Python objects into the cache
- Supports Memcache, Redis and SQLite
- Provides a few handy extras
  - A plugin for the [cachecontrol](https://pypi.org/project/CacheControl/) library so you can also use it as an HTTP cache with [requests](https://pypi.org/project/requests/)

## A simple example

```python
from datetime import date

from pyappcache.memcache import MemcacheCache
from pyappcache.keys import GenericStringKey

cache = MemcacheCache()
key = GenericStringKey("mifid start date")
cache.set(key, date(2018, 1, 3), ttl=3600)

... # later...

special_date = cache.get(key)
```
