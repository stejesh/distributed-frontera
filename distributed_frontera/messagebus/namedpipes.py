# -*- coding: utf-8 -*-

from base import BaseSpiderFeedStream, BaseStreamConsumer
from distributed_frontera.worker.partitioner import Crc32NamePartitioner
from os import mkfifo, open, close, read, write, O_NONBLOCK, O_RDONLY, O_WRONLY
from os.path import exists
from struct import pack, unpack
from errno import EAGAIN, EWOULDBLOCK
from io import BytesIO
from time import sleep, clock


ROOT = "/Users/sibiryakov/local/frontera"

def get_path(partition):
    return ROOT + "/main%d.pipe" % partition

class StreamConsumer(BaseStreamConsumer):
    def __init__(self, partition_id):
        self.fd = open(get_path(partition_id), O_NONBLOCK | O_RDONLY)
        self.buffer = BytesIO()

    def get_message(self, timeout=0.1, count=1):
        result = []
        start_time = clock()
        while len(result) < count:
            try:
                buffer = read(self.fd, 4096)
            except OSError as err:
                if err.errno == EAGAIN or err.errno == EWOULDBLOCK:
                    buffer = None
                else:
                    raise

            if buffer is None:
                if start_time + timeout < clock():
                    sleep(0.1)
                    continue
                else:
                    return result

            self.buffer.write(buffer)


        stream = BytesIO(self.buffer)
        length = unpack('>I', stream.read(4))[0]
        message = stream.read(length)
        result.append(message)





    def close(self):
        close(self.fd)


class Producer(object):
    def __init__(self, partitions, partitioner):
        self.partitioner = partitioner
        self.fd = {}
        for partition_id in partitions:
            self.fd[partition_id] = open(get_path(partition_id), O_NONBLOCK | O_WRONLY)

    def put(self, message, key):
        partition_id = self.partitioner.partition(key)
        fd = self.fd[partition_id]
        write(fd, pack('>I', len(message)))
        write(fd, message)

    def close(self):
        for fd in self.fd.values(): close(fd)

class SpiderFeedStream(BaseSpiderFeedStream):

    partitions = [0, 1, 2, 3]
    def __init__(self):
        self.partitioner = Crc32NamePartitioner(self.partitions)
        for partition in self.partitions:
            path = get_path(partition)
            if not exists(path):
                mkfifo(path)

    def consumer(self, partition_id):
        return StreamConsumer(partition_id)

    def put(self, message, key):


