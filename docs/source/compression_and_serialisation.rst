Compressiong and serialisation
==============================

Pyappcache offers pluggable compression and serialisation so you can choose
what is used to compress your cache values and how they are serialised.  The
defaults are gzip and pickle.

Compression
-----------

.. autoclass:: pyappcache.compression.DefaultGZIPCompressor


Serialisation
-------------

.. autoclass:: pyappcache.serialisation.PickleSerialiser
