# -*- coding: utf-8 -*-
from abc import abstractmethod, abstractproperty, ABCMeta

class BaseStreamConsumer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, partition_id):
        pass

    @abstractmethod
    def get_message(self, timeout=0.1, count=1):
        """
        :return: raw message
        """
        raise NotImplementedError


class BaseSpiderLogStream(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, partitioner):
        pass

    @abstractmethod
    def put(self, message, key):
        """
        Using FingerprintPartitioner (because of state cache in Strategy Workers)
        :param message: str, encoded message
        :param key: str
        """
        raise NotImplementedError

    @abstractmethod
    def consumer(self, partition_id, group):
        """
        Messages consumed by all known groups can be freed
        :param partition_id: int
        :param group: consumer group
        :return: BaseStreamConsumer instance assigned to given partition_id
        """
        raise NotImplementedError


class BaseUpdateScoreStream(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self):
        """
        :return: str encoded message
        """
        raise NotImplementedError

    @abstractmethod
    def put(self, message):
        """
        :param message: encoded message
        """
        raise NotImplementedError


class BaseSpiderFeedStream(object):
    @abstractmethod
    def __init__(self, partitioner):
        pass

    @abstractmethod
    def consumer(self, partition_id):
        """
        :param partition_id:
        :return: BaseStreamConsumer instance assigned to given partition_id
        """
        raise NotImplementedError

    @abstractmethod
    def put(self, message, key):
        """
        Using Crc32NamePartitioner
        :param message: str encoded message
        :param key: str
        """
        raise NotImplementedError

    @abstractmethod
    def available_partitions(self):
        """
        :return: list of ints
        """
        raise NotImplementedError


class BaseMessageBus(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def update_score(self):
        """
        :return: instance of UpdateScoreStream
        """
        raise NotImplementedError

    @abstractproperty
    def spider_log(self):
        """
        :return: instance of SpiderLogStream
        """
        raise NotImplementedError

    @abstractproperty
    def spider_feed(self):
        """
        :return: instance of SpiderFeedStream
        """
        raise NotImplementedError