#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-22 11:18:48
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json

with open('tw_edu.json') as fd:
    edu = json.load(fd)

vv = dict()
with open('variants.txt') as fd:
    for line in fd:
        line = line.strip().split()
        c1, c2 = line[0], line[1]
        if c1 in vv:
            vv[c1].append(c2)
        else:
            vv[c1] = [c2,]

with open('z2.txt') as fd:
    for line in fd:
        line = line.strip().split()
        c1, c2 = line[0], line[1]
        c2x = "U+%X" % ord(c2)
        # if c1 in edu and c2 not in edu and not c2x.startswith('U+F'):
        #     print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))
        vv[c1].append(c2)
        # if c1 in vv and c2 not in vv[c1]:
        #     print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))
        # if c1 not in edu and c2 not in edu:
        #    print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))

result = set()

for i in vv:
    vv[i] = sorted(vv[i], key=lambda x: ord(x))

for i in vv:
    for j in vv[i]:
        result.add((i, j))

result = sorted(list(result), key=lambda x: ord(x[0]))

for c1,c2 in result:
    print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))



def main():
    ''''''





def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

