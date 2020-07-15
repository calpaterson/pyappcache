pyappcache
==========

Pyappcache is a library to make it easier to use application-level
caching in Python.

-  Allows putting arbitrary Python objects into the cache

   -  And provides type hints so you can typecheck what you get back
      from the cache

-  Supports Memcache, Redis and SQLite
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
