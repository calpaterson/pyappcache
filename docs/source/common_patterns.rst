Common patterns
===============

Using pyappcache to provide caching for ``requests``
----------------------------------------------------

Pyappcache provides some added extras to allow it to be used as a cache for the
popular `requests <https://requests.readthedocs.io/en/master/>`_ library when
used in conjunction with the `CacheControl
<https://cachecontrol.readthedocs.io/en/latest/>`_ library.

CacheControl provides the HTTP caching logic and Pyappcache provides the cache
backends.

.. autoclass:: pyappcache.util.requests.CacheControlProxy

.. code:: python

    import requests
    import cachecontrol
    from pyappcache.redis import RedisCache
    from pyappcache.util.requests import CacheControlProxy

    # Create a Cache instance around Redis
    cache = RedisCache()

    # Create the proxy, which implements CacheControl's desired API
    cc_proxy = CacheControlProxy(cache)

    # Create the session
    cached_session = cachecontrol.CacheControl(
        requests.Session(),
        cache=cc_proxy
    )

    # Make the request - first time not cached
    cached_session.get("http://calpaterson.com")

    # Make the request - seen it before so reads from cache
    cached_session.get("http://calpaterson.com")


Storing your cache in a local sqlite file
-----------------------------------------

.. _local sqlite file as cache:

Sometimes it's handy to have the cache stored on disk.  This is not as fast as
in-memory but can be handy if you need a way to persist cache entries but
aren't able to run a "proper" cache server like memcache or redis.

.. code:: python

    import sqlite3
    from pyappcache.sqlite_lru import SqliteCache

    sqlite_db = sqlite3.connect("my_cache.sqlite3")
    cache = SqliteCache(connection=sqlite_db)
