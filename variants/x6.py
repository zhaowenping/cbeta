#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-06-22 10:35:17
from __future__ import unicode_literals, division, absolute_import, print_function

"""
将异体字字典改成横排形式
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import json


rr = dict()
with open('variants.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip()
        if not line: continue
        data = line.split()
        c1 = data[0]
        c2 = data[1]

        if c1 in rr:
            rr[c1].append(c2)
        else:
            rr[c1] = [c2,]

# result = sorted(list(result), key=lambda x: ord(x[0]))
rk = sorted(rr.keys(), key=lambda x: ord(x))

for c1 in rk:
    try:
        cc = sorted([i for i in rr[c1]], key=lambda x: ord(x))
    except:
        print(c1, rr[c1])
        raise
    cc.insert(0, c1)
    print(','.join(cc))
    # for c2 in cc:
    #     # if c1 in edu and c2 in edu:
    #     if c1 != c2:
    #         print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))

# print(data)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

