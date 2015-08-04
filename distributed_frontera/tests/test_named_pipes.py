# -*- coding: utf-8 -*-
from distributed_frontera.messagebus.namedpipes import SpiderFeedStream
from random import choice, randint
from sys import stdout


def _get_random_string():
    size = randint(8, 64)
    result = str()
    for i in range(size):
        result += choice('abcdefghijklmnopqrstuvwxyz')
    return result

def test_produce_consume():
    sf = SpiderFeedStream()

    p = sf.producer()
    while True:
        for key in [0, 1, 2, 3, 4, 5]:
            p.put("abcdefghijklmn", str(key))
test_produce_consume()
