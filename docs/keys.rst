Keys
====

Why Key classes?
----------------

The advantage of making cache keys first class objects:

#. Encapsulate all the logic for calculating the key in one place
#. Allow for typechecking return values from the cache
#. Make it possible to control compression, namespacing, etc in one place

A note on "key paths"
^^^^^^^^^^^^^^^^^^^^^

Pyappcache is designed around the idea of "key paths" that are predictable and
similar to unix paths, such as `users/54/likes`, which might store user number
54's likes.  Predictable key paths aid debugging - you can always guess where
to look when using the cache separately from pyappcache.

Pyappcache caches will also *prefix* key paths with some custom key path, to
allow multiple different uses of the same cache without each clobbering the
other's namespace.

How to create your own key classes
----------------------------------

Option 1: Simple string keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you just want to use a string as your key, you can use :class:`~pyappcache.keys.SimpleStringKey`.

.. autoclass:: pyappcache.keys.SimpleStringKey
               :members: __init__

.. code:: python

    from pyappcache.keys import SimpleStringKey

    death_star_location = SimpleStringKey("death-star-location")
    cache.set(death_star_location, "near alderaan")

    ... # later...
    where_is_it_now = cache.get(death_star_location)

Option 2: Subclasses of BaseKey
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to have something more complicated, you can often get started by
subclassing :class:`~pyappcache.keys.BaseKey`.

.. autoclass:: pyappcache.keys.BaseKey
               :members: cache_key_segments

This abstract base class is designed to make it quick as possible to create a
new key class - just override `cache_key_segments` and you're ready to go.

Option 3: Something more complicated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want full flexibilty you need only define three special methods to allow
any object to act as a `Key`.

.. autoclass:: pyappcache.keys.Key
               :members: namespace_key, should_compress, cache_key_segments
