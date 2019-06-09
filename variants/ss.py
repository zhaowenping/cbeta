#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-06-07 21:10:19
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


shuzi = list()
with open('shuzi.txt') as fd:
    for line in fd:
        line = line.strip()
        shuzi.append(line)

cipin = dict()
with open('../../cp.txt') as fd:
    for line in fd:
        line = line.strip().split()
        zi = line[0]
        cipin[zi] = int(line[2])

shuzi = ''.join(shuzi)
shuzi = sorted(shuzi, key=lambda x: ord(x))

for zi in shuzi:
    print(zi, 'U+%X' % ord(zi), cipin.get(zi, 0))

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

