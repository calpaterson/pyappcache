Caches
======

The common interface
--------------------

There is support for a few caches built-in: memcache, redis and a sqlite-based
LRU cache.  They all share a common interface to make it easier to swap them in
an out.

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

Storing your cache in a local sqlite file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes it's handy to have the cache stored on disk.  This is not as fast as
in-memory but can be handy if you need a way to persist cache entries but
aren't able to run a "proper" cache server like memcache or redis.

.. code:: python

    import sqlite3
    from pyappcache.sqlite_lru import SqliteCache

    sqlite_db = sqlite3.connect("my_cache.sqlite3")
    cache = SqliteCache(connection=sqlite_db)

Implementing support for your own cache
---------------------------------------

FIXME: hints on what methods to implement
