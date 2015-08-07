=================
Crawling strategy
=================

Use ``distributed_frontera.worker.strategy.bfs`` module for reference. In general, you need to write a
``CrawlingStrategy`` class with above interface::

    class CrawlStrategy(object):
        def __init__(self):
            pass

        def add_seeds(self, seeds):
            pass

        def page_crawled(self, response, links):
            pass

        def page_error(self, request, error):
            pass

        def finished(self):
            return False

        def get_score(self, url):
            return 1.0

All the incoming results from spiders will be passed through this interface and for each URL the score should be
calculated and returned by method ``get_score``. Periodically ``finished()`` method is called to check if crawling goal
is achieved. The strategy class instantiated in strategy worker, and can use it's own storage or any other kind of
resources.

