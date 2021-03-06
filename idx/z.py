#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2021-03-06 06:57:22
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re

ids_dict = dict()
with open('ids.txt') as fd:
    for line in fd:
        line = line.strip().split()
        ids_dict[line[2]] = line[1]
#print(ids_dict.keys())
z = sorted(ids_dict.keys(), key=len, reverse=True)
p = re.compile('|'.join(sorted(ids_dict.keys(), key=len, reverse=True)))
#re.compile(z)
for i in range(28506):
    x = '|'.join(z[i:i+1])
    try:
        re.compile(x)
    except re.error as e:
        print(z[i:i+1])
    continue

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

