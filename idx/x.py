#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2021-03-05 16:37:17
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

ids_dict = dict()
with open('ids.txt') as fd:
    for line in fd:
        line = line.strip().split()
        bj = set(line[2])
        for i in bj:
            if i not in ids_dict:
                ids_dict[i] = 1
            else:
                ids_dict[i] +=1

for k in ids_dict:
    print(k, ids_dict[k])


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

