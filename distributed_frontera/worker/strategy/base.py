# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class BaseCrawlingStrategy(object):
    """
    Interface definition for a crawling strategy.

    Before calling these methods strategy worker is adding 'state' key to meta field in every
    :class:`Request <frontera.core.models.Request>` with state of the URL. Pleases refer for the states to HBaseBackend
     implementation.

    After exiting from all of these methods states from meta field are passed back and stored in the backend.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_seeds(self, seeds):
        """
        Called when add_seeds event is received from spider log.

        :param list seeds: A list of :class:`Request <frontera.core.models.Request>` objects.
        :return: dict with keys as fingerprints (as hex string) and values as float scores, if no scheduling is needed,
         no fingerprint should be returned
        """
        return {}

    @abstractmethod
    def page_crawled(self, response, links):
        """
        Called every time document was successfully crawled, and receiving page_crawled event from spider log.

        :param object response: The :class:`Response <frontera.core.models.Response>` object for the crawled page.
        :param list links: A list of :class:`Request <frontera.core.models.Request>` objects generated from \
        the links extracted for the crawled page.
        :return: dict with keys as fingerprints (as hex string) and values as float scores, if no scheduling is needed,
         no fingerprint should be returned
        """
        return {}

    @abstractmethod
    def page_error(self, request, error):
        """
        Called every time there was error during page downloading.

        :param object request: The fetched with error :class:`Request <frontera.core.models.Request>` object.
        :param str error: A string identifier for the error.
        :return: dict with one key as fingerprint (as hex string) and value as float score, if no scheduling is needed,
         empty dict should be returned
        """
        return {}

    @abstractmethod
    def finished(self):
        return False