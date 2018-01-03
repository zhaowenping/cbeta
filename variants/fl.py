#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-01-02 20:25:46
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import gzip
import json


yitizi = dict()
with open('variants.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip().split()
        yitizi[ord(line[1])] = ord(line[0])

def normyitizi(string, level=0):
    '''异体字规范化为标准繁体字'''
    string = string.translate(yitizi)
    return string

with gzip.open('../dict/dfb.json.gz') as fd:
    dfb = json.load(fd)

result = set()
for zi in dfb:
    if zi != normyitizi(zi):
        a = set(zi) - set(normyitizi(zi))
        b = set(normyitizi(zi)) - set(zi)
        if len(a) == 1:
            a = list(a)[0]
            b = list(b)[0]
            if a > b:
                result.add(' '.join((a, b)))
            else:
                result.add(' '.join((b, a)))
        else:
            result.add((tuple(b), tuple(a)))

import pprint
for i in result:
    print(i)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

