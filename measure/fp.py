#! /usr/bin/env python
# vim: set fileencoding=utf-8
from time import sleep
from random import choice


if __name__ == '__main__':
    map(lambda x: x**8-5, range(int(.5e5)))
    sleep(0.1)
    if choice([True, False]):
        print "yes 2 3 5"
    else:
        print "no"
