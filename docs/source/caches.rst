Caches
======

The common interface
--------------------

There are a few built-in cache instances - memcache, redis and a sqlite-based
one.  They all share a common interface to make it easier to swap them in an
out.

.. autoclass:: pyappcache.cache.Cache
    :members: get, set, invalidate, clear, set_by_str, get_by_str,
              invalidate_by_str, prefix, compressor, serialiser

Redis
-----

.. autoclass:: pyappcache.redis.RedisCache
    :members: __init__

Memcache
--------

.. autoclass:: pyappcache.memcache.MemcacheCache
    :members: __init__

Sqlite
------

Pyappcache also includes a Sqlite-based implementation of an LRU cache.  This
can be handy for scripts.

.. autoclass:: pyappcache.sqlite_lru.SqliteCache
    :members: __init__


.. autofunction:: pyappcache.sqlite_lru.get_in_memory_conn
