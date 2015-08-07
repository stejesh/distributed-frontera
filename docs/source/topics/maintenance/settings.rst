========
Settings
========

Distributed Frontera uses the same settings mechanism as Frontera, redefines some of the default values and introduces
new settings.

.. _distributed-frontera-settings:


Redefined default values
========================

.. setting:: DELAY_ON_EMPTY

DELAY_ON_EMPTY
--------------

Default: ``30.0``

Delay between calls to backend for new batches in Scrapy scheduler, when queue size is getting below
``CONCURRENT_REQUESTS``.

.. setting:: OVERUSED_SLOT_FACTOR

OVERUSED_SLOT_FACTOR
--------------------

Default: ``2.0``

(in progress + queued requests in that slot) / max allowed concurrent downloads per slot before slot is considered
overused. This affects only Scrapy scheduler.


.. setting:: URL_FINGERPRINT_FUNCTION

URL_FINGERPRINT_FUNCTION
------------------------

Default: ``frontera.utils.fingerprint.hostname_local_fingerprint``

This function is used for URL fingerprinting, which serves to uniquely identify the document in storage.
``hostname_local_fingerprint`` is constructing fingerprint getting first 4 bytes as Crc32 from host, and rest is MD5
from rest of the URL. Default option is set to make use of HBase block cache. It is expected to fit all the documents
of average website within one cache block, which can be efficiently read from disk once.


Built-in settings
=================

Here’s a list of all available Distributed Frontera settings, in alphabetical order, along with their default values
and the scope where they apply.

.. setting:: HBASE_BATCH_SIZE

HBASE_BATCH_SIZE
----------------

Default: ``9216``

Count of accumulated PUT operations before they sent to HBase.

.. setting:: HBASE_DROP_ALL_TABLES

HBASE_DROP_ALL_TABLES
---------------------

Default: ``False``

Enables dropping and creation of new HBase tables on worker start.

.. setting:: HBASE_METADATA_TABLE

HBASE_METADATA_TABLE
--------------------

Default: ``metadata``

Name of the documents metadata table.

.. setting:: HBASE_NAMESPACE

HBASE_NAMESPACE
---------------

Default: ``crawler``

Name of HBase namespace where all crawler related tables will reside.

.. setting:: HBASE_QUEUE_PARTITIONS

HBASE_QUEUE_PARTITIONS
----------------------

Default: ``4``

Number of partitions in HBase priority queue. Distributed Frontera has one queue partition assigned per spider.
Therefore that number should be equal to the number of spider instances in the cluster.

.. setting:: HBASE_QUEUE_TABLE

HBASE_QUEUE_TABLE
-----------------

Default: ``queue``

Name of HBase priority queue table.

.. setting:: HBASE_STATE_CACHE_SIZE_LIMIT

HBASE_STATE_CACHE_SIZE_LIMIT
----------------------------

Default: ``3000000``

Number of items in the :term:`state cache` of :term:`strategy worker`, before it get's flushed to HBase and cleared.


.. setting:: HBASE_STORE_CONTENT

HBASE_STORE_CONTENT
-------------------

Default: ``False``

Whatever content needs to be stored in HBase. A serious performance killer.


.. setting:: HBASE_THRIFT_HOST

HBASE_THRIFT_HOST
-----------------

Default: ``localhost``

HBase Thrift server host.

.. setting:: HBASE_THRIFT_PORT

HBASE_THRIFT_PORT
-----------------

Default: ``9090``

HBase Thrift server port

.. setting:: HBASE_USE_COMPACT_PROTOCOL

HBASE_USE_COMPACT_PROTOCOL
--------------------------

Default: ``False``

Whatever workers should use Thrift compact protocol. Dramatically reduces transmission overhead, but needs to be turned
on on server too.

.. setting:: HBASE_USE_SNAPPY

HBASE_USE_SNAPPY
----------------

Default: ``False``

Whatever to compress content and metadata in HBase using Snappy. Decreases amount of disk and network IO within HBase,
lowering response times. HBase have to be properly configured to support Snappy compression.





