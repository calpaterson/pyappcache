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

Example code
^^^^^^^^^^^^

.. code:: python

    import requests
    import cachecontrol
    from pyappcache.sqlite_lru import SqliteCache
    from pyappcache.util.requests import CacheControlProxy

    # Create the cache object (in-memory is the default)
    cache = SqliteCache()

    # Create the proxy, which implements CacheControl's desired API
    cc_proxy = CacheControlProxy(cache)

    # Create the session
    cached_session = cachecontrol.CacheControl(requests.Session(), cache=cc_proxy)

    # Make the request - first time not cached
    cached_session.get("http://calpaterson.com")

    # Make the request - seen it before so reads from cache
    cached_session.get("http://calpaterson.com")


Using a local sqlite file as a cache
------------------------------------

See :ref:`local sqlite file as cache`
