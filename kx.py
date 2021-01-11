#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-12-30 07:35:42
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import gzip
import json

with gzip.open('dict/kangxi.json.gz') as fd:
    data = json.load(fd)

cipin = dict()

with open('../p0.txt') as fd:
    for line in fd:
        line = line.strip().split()
        zi, t, cp = line
        cp = int(cp)
        cipin[zi] = cp

# for zi in data:
#     if '國語發音' in data[zi] and zi in cipin:
#         py = data[zi]['國語發音']
#         pys = py.split()
#         if len(pys) > 1:
#             cp = cipin[zi]
#             print(zi, "U+%X" % ord(zi), cp, py)
#     # else:
#     #     print(zi)

result = set()
for zi in data:
    if '國語發音' in data[zi]:
        py = data[zi]['國語發音']
        py = py.split()
        for p in py:
            result.add(p)

import pprint
#pprint.pprint(result)
a = set()
for i in result:
    for j in set(i):
        a.add(j)
for i in a:
    print(i, i)
#print(len(result))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

