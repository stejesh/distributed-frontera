.. distributed-frontera documentation master file, created by
   sphinx-quickstart on Wed Jul 15 20:20:07 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Distributed Frontera: Large-scale web crawling framework
========================================================

`Frontera`_ is a crawl frontier implementation for a `web crawler`_. It's managing when and what to crawl next, checking
 for crawling goal achievement. `Distributed Frontera`_ is extension to Frontera allowing it to replicate, shard and
 isolate all the parts of Frontera-based crawler to solve large scale crawling problems. Both these packages contain
 components to allow creation of fully-operational web crawler with Scrapy.

Contents
========
.. toctree::
    :maxdepth: 2

    topics/overview
    topics/quickstart
    topics/full_scale_deployment

Customizing
-----------
.. toctree::
    :maxdepth: 2

    topics/customization/own_crawling_strategy
    topics/customization/transferring_from_spider
    topics/customization/communication
    topics/customization/extending_sw

Maintenance
-----------
.. toctree::
    :maxdepth: 2

    topics/maintenance/settings
    topics/maintenance/cluster-configuration
    topics/maintenance/rebuilding_queue

Miscellaneous
-------------
.. toctree::

    topics/glossary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
* :doc:``

.. _`Frontera`: http://github.com/scrapinghub/frontera
.. _`web crawler`: https://en.wikipedia.org/wiki/Web_crawler
.. _`Distributed Frontera`: https://github.com/scrapinghub/distributed-frontera
