#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-16 09:57:54
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


# with open('3Sort.txt') as fd:
#     for line in fd:
#         if line.startswith('#'): continue
#         line = line.strip()
#         if not line: continue
#         data = line.split()
#         c1 = data[0]
#         c2 = data[1]
#         c3 = data[2]
#         if c2 in edu or c3 in edu and not (c2 in edu and c3 in edu):
#             if c2 in edu:
#                 print(c1, c2, c3, "U+%X" % ord(c1), "U+%X" % ord(c2), "U+%X" % ord(c3))
#             else:
#                 print(c1, c3, c2, "U+%X" % ord(c1), "U+%X" % ord(c3), "U+%X" % ord(c2))

result = set()
with open('z4.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip()
        if not line: continue
        data = line.split()
        c1 = data[0]
        c2 = data[1]
        # c3 = data[2]
        if c2 not in result:
            result.add(c2)
        else:
            print(c2)

# result = sorted(list(result), key=lambda x: ord(x[0]))
# for c1,c2 in result:
#     print(c1,c2, "U+%X" % ord(c1), "U+%X" % ord(c2))

# print(data)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

