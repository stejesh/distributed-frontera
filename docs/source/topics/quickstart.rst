==========
Quickstart
==========

Here is a guide how to quickly setup Distributed Frontera for single-machine local hacking. Please proceed to
:doc:`full_scale_deployment` for a production setup details.

1. Prerequisites
================

Here is what services needs to be installed and configured before running Frontera:
* Kafka,
* HBase.

These can be setup locally, no specific tuning is needed.

Also you need to have installed Python 2.7+, Scrapy, Frontera and Distributed Frontera libraries.

Frontera installation
---------------------
For Ubuntu: ::


    apt-get install libsnappy-dev
    pip install distributed-frontera


2. Create a simple Scrapy spider
================================
Creation of basic Scrapy spider is described at `Frontier at a glance`_ page. However, for broad crawling please
consider following:

Adding one of seed loaders for bootstrapping of crawling process::

    SPIDER_MIDDLEWARES.update({
        'frontera.contrib.scrapy.middlewares.seeds.file.FileSeedLoader': 1,
    })

Auto throttling and concurrency settings for polite and responsible crawling:::

    # auto throttling
    AUTOTHROTTLE_ENABLED = True
    AUTOTHROTTLE_DEBUG = False
    AUTOTHROTTLE_MAX_DELAY = 3.0
    AUTOTHROTTLE_START_DELAY = 0.25
    RANDOMIZE_DOWNLOAD_DELAY = False

    # concurrency
    CONCURRENT_REQUESTS = 128
    CONCURRENT_REQUESTS_PER_DOMAIN = 10
    DOWNLOAD_DELAY = 0.0

It's also a good practice to prevent spider from closing because of insufficiency of queued requests transport:::

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self):
        self.log("Spider idle signal caught.")
        raise DontCloseSpider

4. Configure Frontera workers
=============================
There are two type of workers: Storage and Strategy.

Storage worker is responsible for communicating with storage DB, and mainly saving metadata and content along with
retrieving new batches to download.

Strategy worker is reading :term:`spider log`, calculating score, deciding if URL needs to be crawled and
pushes scores to :term:`scoring log`.

Now, let's create a Frontera workers settings file under ``frontera`` subfolder and name it ``worker_settings.py``.::

    from distributed_frontera.settings.default_settings import MIDDLEWARES

    MAX_REQUESTS = 0
    MAX_NEXT_REQUESTS = 128     # Size of batch to generate per partition, should be consistent with
                                # CONCURRENT_REQUESTS in spider. General recommendation is 5-7x CONCURRENT_REQUESTS
    CONSUMER_BATCH_SIZE = 512   # Batch size for updates to backend storage
    NEW_BATCH_DELAY = 30.0      # This cause spider to wait for specified time, after getting empty response from
                                # backend

    #--------------------------------------------------------
    # Url storage
    #--------------------------------------------------------
    BACKEND = 'distributed_frontera.contrib.backends.hbase.HBaseBackend'
    HBASE_DROP_ALL_TABLES = False
    HBASE_THRIFT_PORT = 9090
    HBASE_THRIFT_HOST = 'localhost'
    HBASE_QUEUE_PARTITIONS = 2  # Count of spider instances

    MIDDLEWARES.extend([
        'frontera.contrib.middlewares.domain.DomainMiddleware',
        'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
    ])

    KAFKA_LOCATION = 'localhost:9092'
    FRONTIER_GROUP = 'scrapy-crawler'
    INCOMING_TOPIC = 'frontier-done'    # Topic used by spiders where to send fetching results
    OUTGOING_TOPIC = 'frontier-todo'    # Requests that needs to be downloaded is written there
    SCORING_GROUP = 'scrapy-scoring'
    SCORING_TOPIC = 'frontier-score'    # Scores provided by strategy worker using this channel and read by storage
                                        # worker.

    #--------------------------------------------------------
    # Logging
    #--------------------------------------------------------
    LOGGING_EVENTS_ENABLED = False
    LOGGING_MANAGER_ENABLED = True
    LOGGING_BACKEND_ENABLED = True
    LOGGING_DEBUGGING_ENABLED = False


5. Configure Frontera spiders
=============================
Next step is to create own file Frontera settings file for every spider instance, in this guide we're going to have 2.
It is recommended to name settings file according to partition ids assigned. E.g. ``settingsN.py``. ::

    from distributed_frontera.settings.default_settings import MIDDLEWARES

    MAX_REQUESTS = 0
    MAX_NEXT_REQUESTS = 256     # Should be consistent with MAX_NEXT_REQUESTS set for Frontera worker

    MIDDLEWARES.extend([
        'frontera.contrib.middlewares.domain.DomainMiddleware',
        'frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware'
    ])

    #--------------------------------------------------------
    # Crawl frontier backend
    #--------------------------------------------------------
    BACKEND = 'distributed_frontera.backends.remote.KafkaOverusedBackend'
    KAFKA_LOCATION = 'localhost:9092'     # Your Kafka service location
    SPIDER_PARTITION_ID = 0      # Partition ID assigned

    #--------------------------------------------------------
    # Logging
    #--------------------------------------------------------
    LOGGING_ENABLED = True
    LOGGING_EVENTS_ENABLED = False
    LOGGING_MANAGER_ENABLED = False
    LOGGING_BACKEND_ENABLED = False
    LOGGING_DEBUGGING_ENABLED = False

You should end up having as much settings files as your system spider instances will have. You can also store permanent
options in common module, and import it's contents from each instance-specific config file.

6. Create Kafka topics
======================
The main thing to do here is to set the number of partitions for ``OUTGOING_TOPIC`` equal to the number of spider
instances. For other topics it makes sense to set more than one partition to better distribute the load across Kafka
cluster.

7. Start cluster
================

First, let's start storage worker. It's recommended to dedicate one worker instance for new batches generation and
others for the rest. Batch generation instance isn't much dependent on the count of spider instances, but saving
to storage is.::

    # start the batch generation and DB saving instance
    $ python -m distributed_frontera.worker.main --config frontera.worker_settings


Next, let's start strategy worker with sample strategy for crawling the internet in Breadth-first manner.::

    $ python -m distributed_frontera.worker.score --config frontera.worker_settings --strategy
        distributed_frontera.worker.strategy.bfs

You should notice that all processes are writing messages to the output. It's ok if nothing is written in Kafka topics,
because of absence of seed URLs in the system.

Let's put our seeds in text file, one URL per line.
Starting the spiders:::

    $ scrapy crawl tutorial -L INFO -s FRONTERA_SETTINGS=frontera.settings0 -s SEEDS_SOURCE = 'seeds.txt'
    ...
    $ scrapy crawl tutorial -L INFO -s FRONTERA_SETTINGS=frontera.settings1
    $ scrapy crawl tutorial -L INFO -s FRONTERA_SETTINGS=frontera.settings2
    $ scrapy crawl tutorial -L INFO -s FRONTERA_SETTINGS=frontera.settings3
    ...
    $ scrapy crawl tutorial -L INFO -s FRONTERA_SETTINGS=frontera.settingsN

You should end up with N spider processes running. Each should read it's own Frontera config, and first one is using
``SEEDS_SOURCE`` variable to pass seeds to Frontera cluster.

After some time seeds will pass the Kafka topics and get scheduled for downloading by workers. Crawler is bootstrapped.

.. _`Frontier at a glance`: http://frontera.readthedocs.org/en/latest/topics/frontier-at-a-glance.html
