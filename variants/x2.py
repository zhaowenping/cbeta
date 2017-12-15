#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-15 15:50:20
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

result = dict()
rr = []

with open('1Sorted.json') as fd:
    for line in fd:
        line = line.strip()
        data = line.split()
        # if data[0] in result:
        #     print(line)
        # else:
        #     result[data[0]] = data[1]
        rr.append((data[0], data[1]))
        result[data[1]] = data[0]

# f900~fad9
# rr = sorted(rr, key=lambda x: ord(x[1]))
# for i in rr:
#     print(i[0], i[1], "U+%X" % ord(i[0]), "U+%X" % ord(i[1]))
#
for i in range(0xf900, 0xfada):
    cc = chr(i)
    if cc in result:
        print(result[cc], cc, "U+%X" % ord(result[cc]), "U+%X" % i)
    else:
        print('  ', cc, "  ", "U+%X" % i)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

