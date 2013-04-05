#! /usr/bin/python
# vim: set fileencoding=utf-8
import sys


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        first_line = f.readline().strip()

    if first_line.startswith('#'):
        gold = first_line[2:]
    else:
        gold = "no"

    with open('gold', 'w') as f:
        f.write(gold)
