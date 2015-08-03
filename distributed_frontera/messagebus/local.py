# -*- coding: utf-8 -*-


class SpiderLogStream(object):
    def __init__(self, in_partition_id):
        pass

    def get(self):
        pass

    def put(self, message, key):
        # using FingerprintPartitioner
        pass


class UpdateScoreStream(object):
    def get(self):
        pass

    def put(self, message):
        pass


class SpiderFeedStream(object):
    def __init__(self, in_partition_id):
        pass

    def get(self):
        pass

    def put(self, message, key):
        # using Crc32NamePartitioner
        pass


class MessageBus(object):
    @property
    def update_score(self):
        pass

    @property
    def spider_log(self):
        pass

    @property
    def spider_feed(self):
        pass