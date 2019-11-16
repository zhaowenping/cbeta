#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-11-13 06:12:05
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


def readdb(path, trans=False, rev=False):
    '''读取文本数据库, trans为是否用于tanslate函数, rev为是否翻转'''
    result = dict()
    with open(path) as fd:
        for line in fd:
            line = line.strip()
            if line.startswith('#') or not line: continue
            c0, c1, *cc = line.strip().split()
            if trans:
                if rev:
                    result[ord(c1)] = ord(c0)
                else:
                    result[ord(c0)] = ord(c1)
            else:
                if rev:
                    result[c1] = c0
                else:
                    result[c0] = c1
    return result


with open('TSCharacters.txt') as fd:
    for line in fd:
        line = line.strip().split()
        if len(line) == 2:
            c1, c2 = line
            if c1 == c2:
                print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))
        # elif len(line) == 3:
        #     c1, c2, c3 = line
        #     print(c1, c2, c3, "U+%X" % ord(c1), "U+%X" % ord(c2))
        # else:
        #     print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', line)


#print(readdb('TSCharacters.txt'))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

