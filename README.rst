pyappcache
==========

Pyappcache is a library to make it easier to use application-level
caching in Python.

-  Allows putting arbitrary Python objects into the cache
-  Uses PEP484 type hints to help you typecheck cache return values
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

    from pyappcache.redis import RedisCache
    from pyappcache.keys import Key, SimpleStringKey

    cache = RedisCache()

    # Annotate the type here to let mypy know this key is used for dates
    key: Key[date] = SimpleStringKey("mifid start date")
    cache.set(key, date(2018, 1, 3), ttl_seconds=3600)

    ... # later...

    # This variable's type will be inferred as datetime.date
    special_date = cache.get(key)


How it compares to alternatives
-------------------------------

Using the redis/memcache/sqlite client directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Explicit key objects allow for type inference and encapsulation of keying
- Keys are prefix to help prevent collisions
- Optional, pluggable, compression
- Hopefully the overhead is small (not yet tested!)
- Portable between redis/memcache/sqlite, etc

dogpile.cache
~~~~~~~~~~~~~

- Explicit key objects allow for type inference and encapsulation of keying
- dogpile.cache provides locking, pyappcache does not
- Reduced temptation to use the problematic decorator pattern
  - This often causes import order problems as you need to have your cache at import time
- Pyappache doesn't provide DBM/file backends, SQLite instead
