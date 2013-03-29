#! /usr/bin/python
# vim: set fileencoding=utf-8
from multiprocessing import Process, Queue
import time


def find(q, g, what, when):
    time.sleep(when)
    q.put((what, range(5)))

if __name__ == '__main__':
    q = Queue()
    pool = []
    pool.append(Process(target=find, args=(q, None, False, 0.3)))
    pool.append(Process(target=find, args=(q, None, False, 0.8)))
    pool.append(Process(target=find, args=(q, None, True, 1.3)))
    pool.append(Process(target=find, args=(q, None, False, 1.9)))
    for p in pool:
        p.start()
    while True:
        exist, path = q.get()
        if exist:
            for p in pool:
                p.terminate()
            print path
            break
