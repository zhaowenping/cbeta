#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-12-14 18:36:00
from __future__ import unicode_literals, division, absolute_import, print_function

"""
检测文件合法性
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import json

with open('../../cipin.json') as fd:
    cipin = json.load(fd)

with open('tw_edu.json') as fd:
    edu = json.load(fd)



result = set()
r1 = set()
r2 = set()
rr = dict()
with open('variants.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip()
        if not line: continue
        data = line.split()
        c1 = data[0]
        c2 = data[1]
        # c3 = data[2]
        if c1 in rr:
            rr[c1].append(c2)
        else:
            rr[c1] = [c2,]
        r1.add(c1)
        r2.add(c2)
        # if c1 in edu and c2 in edu:
        #     if cipin.get(c1, 0) < cipin.get(c2, 0):
        #         print(c1, c2, cipin.get(c1, 0), cipin.get(c2, 0))

        # if c1 not in edu and c2 not in edu:
        #     if cipin.get(c1, 0) < cipin.get(c2, 0):
        #         print(c1, c2, cipin.get(c1, 0), cipin.get(c2, 0), "%X" % ord(c1), "%X" % ord(c2))

        # result.add((c1, c2))
        # else:
        #     print(c2)

# result = sorted(list(result), key=lambda x: ord(x[0]))
rk = sorted(rr.keys(), key=lambda x: ord(x))

for c1 in rk:
    cc = sorted([i for i in rr[c1]], key=lambda x: ord(x))
    for c2 in cc:
        if c1 not in edu and c2 in edu:
        # if c1 != c2:
            print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2), cipin.get(c1, 0), cipin.get(c2, 0))

for c1 in r1:
    if c1 in r2:
        print(c1, rr[c1])

for c2 in r2:
    if c2 in r1:
        print(c1, rr[c1])

# print(data)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

