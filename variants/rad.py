#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2021-09-05 01:49:42
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

with open('radical.txt') as fd:
    for line in fd:
        line = line.split()
        print(line[0], 'U+%X' % ord(line[0]), int(line[1]))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

