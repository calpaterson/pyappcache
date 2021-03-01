Rationale
=========

Pyappcache takes a slightly different approach to other cache libraries.

First class key objects
-----------------------

In pyappcache, keys are first class objects - though you can use strings too if
you prefer.

Make keys a first class object to make it easier to centralise logic around
keying and avoid typos and other common mistakes that arise when using strings
as keys.

Support multiple caches
-----------------------

Redis and Memcache are both popular volatile caches.  Pyappcache also includes
an implementation using Sqlite can be useful in some scenarios.

It's also easy(ish) to implement support for a new cache.

Support type hints
------------------

Pyappcache has type hinting to help catch bugs - particularly the common
mistake of forgetting that the cache might return nothing!

Pluggable serialisation and compression
---------------------------------------

The specifics of how Python objects are turned into bytestrings is explicit and
pluggable - you can provide your own compression and serialisation methods.

Inspectable
-----------

Pyappcache generates predictable cache keys to make debugging easier - you'll
be able to predict what key is generated (and if you don't know, you can ask a
key object in a REPL).
