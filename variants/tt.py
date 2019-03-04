#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-03-03 08:06:38
from __future__ import unicode_literals, division, absolute_import, print_function

"""
检测文件合法性
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import json

#with open('../../cipin.json') as fd:
#    cipin = json.load(fd)
cipin = dict()
with open('../../cp.txt') as fd:
    for line in fd:
        line = line.strip().split()
        cipin[line[0]] = int(line[2])

with open('tw_edu.json') as fd:
    edu = json.load(fd)



result = list()
with open('variants.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip()
        if not line: continue
        data = line.split()
        c1 = data[0]
        c2 = data[1]
        result.append((c1, c2, cipin.get(c2, 0)))

result = sorted(result, key = lambda x:x[2], reverse=True)
for zi in result:
    print(zi)


# print(data)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

