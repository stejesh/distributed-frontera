==========
Quickstart
==========

Here is a guide how to quickly setup Frontera for single-machine, multiple process, local hacking. Please proceed to
:doc:`production` for a production setup details.

.. _basic_requirements:

Prerequisites
=============

Here is what services needs to be installed and configured before running Frontera:

- Kafka,
- HBase.

These can be set up locally, no specific tuning is needed.
Also you need to have installed Python 2.7+ and Scrapy library.

Frontera installation
---------------------
For Ubuntu, type in command line: ::

    $ apt-get install libsnappy-dev
    $ pip install distributed-frontera


Checkout a simple Scrapy spider
===============================
This is a general spider, it does almost nothing except extracting links from downloaded content. Also contains lots
of predefined options, please consult settings reference to get more information.
::

    $ git clone https://github.com/sibiryakov/general-spider.git

Create Kafka topics
===================
General spider is configured for two spiders and two strategy workers. Therefore incoming and outcoming topic partitions
should be set to 2.

::

    $ kafka-topics.sh --create --topic frontier-todo --replication-factor 1 --partitions 2 --zookeeper localhost:2181
    $ kafka-topics.sh --create --topic frontier-done --replication-factor 1 --partitions 2 --zookeeper localhost:2181
    $ kafka-topics.sh --create --topic frontier-score --replication-factor 1 --partitions 1 --zookeeper localhost:2181

Start cluster
=============

First, let's start DB worker. ::

    $ python -m distributed_frontera.worker.main --config frontier.workersettings


Next, let's start strategy worker with default BFS (Breadth-First Strategy)::

    $ python -m distributed_frontera.worker.score --config frontier.strategy0 --strategy distributed_frontera.worker.strategy.bfs
    $ python -m distributed_frontera.worker.score --config frontier.strategy1 --strategy distributed_frontera.worker.strategy.bfs


You should notice that all processes are writing messages to the output. It's ok if nothing is written in Kafka topics,
because of absence of seed URLs in the system.

There are spanish internet URLs from DMOZ directory in general spider repository, let's use them as seeds to bootstrap
crawling.
Starting the spiders:::

    $ scrapy crawl general -L INFO -s FRONTERA_SETTINGS=frontera.spider0 -s SEEDS_SOURCE=seeds_es_dmoz.txt
    $ scrapy crawl general -L INFO -s FRONTERA_SETTINGS=frontera.spider1


You should end up with 2 spider processes running. Each should read it's own Frontera config, and first one is using
``SEEDS_SOURCE`` variable to pass seeds to Frontera cluster.

After some time seeds will pass the Kafka topics and get scheduled for downloading by workers. At this moment crawler
is bootstrapped. Now you can periodically check DB worker output or ``metadata`` table contents to see that there is
actual activity.
