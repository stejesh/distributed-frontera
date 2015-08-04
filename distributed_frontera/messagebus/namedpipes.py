# -*- coding: utf-8 -*-

from base import BaseSpiderFeedStream, BaseStreamConsumer
from distributed_frontera.worker.partitioner import Crc32NamePartitioner
from os import mkfifo, open, close, read, write, O_NONBLOCK, O_RDONLY, O_WRONLY
from os.path import exists
from struct import pack, unpack_from
from errno import EAGAIN, EWOULDBLOCK
from io import BytesIO, SEEK_CUR, SEEK_END
from time import sleep, clock


ROOT = "/Users/sibiryakov/local/frontera"

def get_path(partition):
    return ROOT + "/main%d.pipe" % partition

class StreamConsumer(BaseStreamConsumer):

    fetch_buffer_size = 4096
    max_buffer_size = 16777216

    def __init__(self, partition_id):
        self.fd = open(get_path(partition_id), O_NONBLOCK | O_RDONLY)
        self.buffer = BytesIO()

    def get_messages(self, timeout=0.1, count=1):
        result = []
        start_time = clock()
        while len(result) < count:
            try:
                buffer = read(self.fd, self.fetch_buffer_size)
            except OSError as err:
                if err.errno == EAGAIN or err.errno == EWOULDBLOCK:
                    buffer = None
                else:
                    raise

            if buffer is None:
                if start_time + timeout > clock():
                    sleep(0.1)
                    print "c"
                    continue
            else:
                position = self.buffer.tell()
                self.buffer.seek(0, SEEK_END)
                self.buffer.write(buffer)
                self.buffer.seek(position)

            raw_length = bytearray(4)
            read_b = self.buffer.readinto(raw_length)
            if read_b != len(raw_length):
                self.buffer.seek(-read_b, SEEK_CUR)
                print "l"
                continue

            length, = unpack_from('>I', raw_length)
            message = self.buffer.read(length)
            if len(message) == length:
                result.append(message)
                #self._reallocate_buffer()
            else:
                print "r", length, len(message)
                self.buffer.seek(-(len(message) + len(raw_length)), SEEK_CUR)
            if start_time + timeout < clock() or len(result) == count:
                break
        return result

    def _reallocate_buffer(self):
        length = len(self.buffer.getvalue())
        if length > self.max_buffer_size:
            print "realloc", length, self.buffer.tell()
            stream = BytesIO(self.buffer.read(length-self.buffer.tell()))
            self.buffer = stream

    def close(self):
        close(self.fd)


class Producer(object):
    def __init__(self, partitions, partitioner):
        self.partitioner = partitioner
        self.fd = {}
        for partition_id in partitions:
            self.fd[partition_id] = open(get_path(partition_id), O_WRONLY)
        self.count = 0

    def put(self, message, key):
        partition_id = self.partitioner.partition(key, None)
        fd = self.fd[partition_id]
        write(fd, pack('>I', len(message)))
        write(fd, message)
        self.count += 1
        if self.count % 1000 == 0:
            print self.count

    def close(self):
        for fd in self.fd.values(): close(fd)


class SpiderFeedStream(BaseSpiderFeedStream):

    partitions = [0]
    def __init__(self):
        self.partitioner = Crc32NamePartitioner(self.partitions)
        for partition in self.partitions:
            path = get_path(partition)
            if not exists(path):
                mkfifo(path)

    def consumer(self, partition_id):
        return StreamConsumer(partition_id)

    def producer(self):
        return Producer(self.partitions, self.partitioner)



