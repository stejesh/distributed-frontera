# -*- coding: utf-8 -*-
from urlparse import urlparse
from crawlfrontier.contrib.canonicalsolvers.basic import BasicCanonicalSolver
from crawlfrontier.contrib.backends.hbase import _state
from base import BaseCrawlingStrategy


class CrawlingStrategy(BaseCrawlingStrategy):
    def __init__(self):
        self.canonicalsolver = BasicCanonicalSolver()

    def add_seeds(self, seeds):
        scores = {}
        for seed in seeds:
            if seed.meta['state'] is None:
                url, fingerprint, _ = self.canonicalsolver.get_canonical_url(seed)
                scores[fingerprint] = 1.0
                seed.meta['state'] = _state.get_id('QUEUED')
        return scores

    def page_crawled(self, response, links):
        scores = {}
        response.meta['state'] = _state.get_id('CRAWLED')
        for link in links:
            if link.meta['state'] is None:
                url, fingerprint, _ = self.canonicalsolver.get_canonical_url(link)
                scores[fingerprint] = self.get_score(url)
                link.meta['state'] = _state.get_id('QUEUED')
        return scores

    def page_error(self, request, error):
        url, fingerprint, _ = self.canonicalsolver.get_canonical_url(request)
        request.meta['state'] = _state.get_id('ERROR')
        return {fingerprint: 0.0}

    def get_score(self, url):
        url_parts = urlparse(url)
        path_parts = url_parts.path.split('/')
        return 1.0 / (max(len(path_parts), 1.0) + len(url_parts.path)*0.1)