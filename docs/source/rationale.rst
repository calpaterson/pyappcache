Rationale
=========

Pyappcache takes a slightly different approach to other cache libraries.

First class key objects
-----------------------

In pyappcache, keys are a first class object (though strings can also be
used).

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

Pyappcache has full type hinting to help cache bugs.  The most useful of these
are likely going to be catching causes where it is assumed that something is
always going to be present and where a different object than expected is being
kept under a key.

Pluggable serialisation and compression
---------------------------------------

The specifics of how Python objects are turned into bytestrings is explicit and
pluggable - you can provide your own compression and serialisation methods.
