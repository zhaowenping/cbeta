#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2023-04-09 20:57:32
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re

ids_dict = list()
with open('ids.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip().split()
        #if 'U+%X' % ord(line[1]) != line[0]:
        #    print(line)
        #ids_dict[line[1]] = line[2]
        ids_dict.append(line)

import pprint
#print(re.compile('|'.join(sorted(ids_dict.keys(), key=len, reverse=True))))
#pprint.pprint(ids_dict)
#ids_dict = sorted(ids_dict, key=lambda x: ord(x[1]))
with open('ids.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip().split()
        for zi in ids_dict:
            if zi[2] == line[2] and  zi[0] != line[0]:
                print(' '.join(zi))

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

