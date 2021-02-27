Caches
======

The standard interface
----------------------

Pyappcache supports multiple different cache backends, all with the same
interface.  No matter whether you're using Redis, Memcache or the SQLiteCache
you will use the same interface:

.. autoclass:: pyappcache.cache.Cache
    :members: get, set, invalidate, clear, set_by_str, get_by_str,
              invalidate_by_str, prefix, compressor, serialiser



Redis
~~~~~

.. autoclass:: pyappcache.redis.RedisCache
    :members: __init__

Memcache
~~~~~~~~

.. autoclass:: pyappcache.memcache.MemcacheCache
    :members: __init__

SqliteCache
~~~~~~~~~~~

Pyappcache also includes a Sqlite-based implementation of an LRU cache.  This
can be handy for scripts.

.. autoclass:: pyappcache.sqlite_lru.SqliteCache
    :members: __init__

.. autofunction:: pyappcache.sqlite_lru.get_in_memory_conn

See :ref:`local sqlite file as cache` for the common pattern of storing the
cache in a file alongside a script.

Implementing support for a custom cache backend
-----------------------------------------------

If you use something else as a cache (a filesystem, some SQL database, dbm)
implementing a custom driver is not too hard.

You need only subclass :class:`~pyappcache.cache.Cache` and implement four
abstract methods:

.. automethod:: pyappcache.cache.Cache.get_raw

.. automethod:: pyappcache.cache.Cache.set_raw

.. automethod:: pyappcache.cache.Cache.invalidate_raw

.. automethod:: pyappcache.cache.Cache.clear
                :noindex:

:class:`~pyappcache.cache.Cache` is implemented entirely in terms of these four
methods so once you implement these, you get everything else "for free".
