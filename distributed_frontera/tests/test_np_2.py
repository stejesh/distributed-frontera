# -*- coding: utf-8 -*-
from distributed_frontera.messagebus.namedpipes import SpiderFeedStream
sf = SpiderFeedStream()
c = sf.consumer(0)
count = 0
while True:
    m = c.get_messages(count=1)
    count += len(m)
    if count % 1000 == 0:
        print count