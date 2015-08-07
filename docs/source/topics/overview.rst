========
Overview
========

Use cases
---------
Broad crawls:
 - arbitrary number of websites and pages

Host-level crawls:
 - more than 100 websites

Focused crawls:
 - topical,
 - PageRank, HITS or other link graph algorithm guided.

Architecture
------------
Overall system forms a closed circle and all the components are working as daemons in infinite cycles.
`Kafka messaging system`_ is used as a data bus, storage is `HBase`_ and fetching is done using `Scrapy`_. Kafka and HBase
are the only options now, but this is going to change in the near future. There are instances of three types:

- **Spiders** or fetchers, implemented using Scrapy (sharded).
    Responsible for resolving DNS queries, getting content from the Internet and doing link (or other data) extraction
    from content.
- **Strategy workers** (sharded).
    Run the crawling strategy code: scoring the links, deciding if link needs to be scheduled and when to stop crawling.
- **DB workers** (replicated).
    Store all the metadata, including scores and content, and generating new batches for downloading by spiders.

Where *sharded* means component consumes messages of assigned partition only, e.g. processes certain share of the topic,
and *replicated* is when components consume topic regardless of partitioning.

Such design allows to operate in real-time. Crawling strategy can be changed without having to stop the crawl. Also
:doc:`crawling strategy <customization/own_crawling_strategy>` can be implemented as a separate module; containing logic for checking the crawling stopping
condition, URL ordering, and scoring model.

Distributed Frontera is polite to web hosts by design and each host is downloaded by no more than one spider process.
This is achieved by Kafka topic partitioning. All Distributed Frontera components are written in Python.

.. image:: images/frontera-design.png

Data flow
---------
Let’s start with spiders. The seed URLs defined by the user inside spiders are propagated to strategy workers and DB
workers by means of a Kafka topic named ‘Spider Log’. Strategy workers decide which pages to crawl using HBase’s state
cache, assigns a score to each page and sends the results to the ‘Scoring Log’ topic.

DB Worker stores all kinds of metadata, including content and scores. DB worker checks for the spider’s consumers
offsets and generates new batches if needed and sends them to “New Batches” topic. Spiders consume these batches,
downloading each page and extracting links from them. The links are then sent to the ‘Spider Log’ topic where they are
stored and scored. That way the flow repeats indefinitely.

.. _`Kafka messaging system`: http://kafka.apache.org/
.. _`HBase`: http://hbase.apache.org/
.. _`Scrapy`: http://scrapy.org/