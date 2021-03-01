Compression and serialisation
==============================

Pyappcache offers pluggable compression and serialisation so you can choose
what is used to compress your cache values and how they are serialised.  The
defaults are gzip and pickle.

Compression
-----------

.. autoclass:: pyappcache.compression.Compressor
               :members: is_compressed, compress, decompress

.. autoclass:: pyappcache.compression.GZIPCompressor
               :members: level


Serialisation
-------------

.. autoclass:: pyappcache.serialisation.Serialiser
               :members: dumps, loads

.. autoclass:: pyappcache.serialisation.PickleSerialiser
               :members: pickle_protocol
