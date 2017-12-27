#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-27 12:59:56
from __future__ import unicode_literals, division, absolute_import, print_function

"""

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
        # result.add((c1, c2))
        # else:
        #     print(c2)

# result = sorted(list(result), key=lambda x: ord(x[0]))
rk = sorted(rr.keys(), key=lambda x: ord(x))

for c1 in rk:
    cc = sorted([i for i in rr[c1]], key=lambda x: ord(x))
    for c2 in cc:
        # if c1 in edu and c2 in edu:
        print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))

# print(data)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

