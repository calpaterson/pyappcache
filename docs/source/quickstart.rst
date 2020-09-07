Quickstart
==========

A minimal example using Redis
-----------------------------

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

The above code:

- creates a new instance of pyappcache's `RedisCache` class
- creates a new key object
- sets that key's value to `date(2018, 1, 3)`
- and then (later) that value can be retrieved *with the right type inference*
