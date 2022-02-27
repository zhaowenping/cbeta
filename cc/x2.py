#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2022-02-22 07:05:05
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


#import opencc
import time

ts = dict()
rr = []
with open('STCharacters.txt') as fd:
    for line in fd:
        # if line.startswith('#'):
        #     print (line)
        line = line.strip().split()
        #if line[0] == line[1]:
        #    print(line)
        if len(line) == 3:
            print(line)
        rr.append(line)
        # ts[line[0]] = line[1:][0]
        ts[ord(line[0])] = ord(line[1:][0])
        #if len(line[1:]) == 2:
        #    print(line)
        #tt.add(line[0])
        #for zi in line[1:]:
        #    ss.add(zi)


# rr = sorted(rr, key= lambda x: ord(x[0]))
# for i in rr:
#     if len(i) == 2:
#         if ord(i[0]) < 0x20000 and ord(i[1]) > 0x20000:
#             print("{} {}, {} {}".format(i[0], i[1], 'U+%X' % ord(i[0]), 'U+%X' % ord(i[1])))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

