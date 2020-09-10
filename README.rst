pyappcache
==========

Pyappcache is a library to make it easier to use application-level
caching in Python.

-  Allows putting arbitrary Python objects into the cache

   -  And provides type hints so you can typecheck what you get back
      from the cache

-  Supports Memcache, Redis and SQLite
-  Supports working as a "read-through" and "write-through" cache
-  Native support for key `"namespacing" <https://github.com/memcached/memcached/wiki/ProgrammingTricks#namespacing>`__
-  Provides a few handy extras

   -  A plugin for the
      `cachecontrol <https://pypi.org/project/CacheControl/>`__ library
      so you can also use it as an HTTP cache with
      `requests <https://pypi.org/project/requests/>`__

A simple example
----------------

.. code:: python

    from datetime import date

    import redis
    from pyappcache.redis import RedisCache
    from pyappcache.keys import Key, GenericStringKey

    client = redis.Redis()
    cache = RedisCache(client)

    # Annotate the type here to let mypy know this key is used for dates
    key: Key[date] = GenericStringKey("mifid start date")
    cache.set(key, date(2018, 1, 3), ttl_seconds=3600)

    ... # later...

    # This variable's type will be inferred as datetime.date
    special_date = cache.get(key)

How it compares to alternatives
-------------------------------

Using the redis/memcache/sqlite client directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Explicit key objects allow for type inference and encapsulation of keying
- Key prefixing
- Optional compression
- Hopefully the overhead is small (not yet tested!)
- Portable between redis/memcache/sqlite, etc

dogpile.cache
~~~~~~~~~~~~~

- Explicit key objects allow for type inference and encapsulation of keying
- As yet there is no locking in pyappcache
- Reduced temptation to use the problematic decorator pattern
  - This often causes import order problems as you need to have your cache at import time
- SQLite backend instead of DBM/file backends
