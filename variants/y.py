#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-01-17 12:42:23
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json

with open('../../cipin.json') as fd:
    cipin = json.load(fd)

# with open('z2all.txt') as fd:
# with open('ytz.txt') as fd:
with open('z2all.txt') as fd:
    for line in fd:
        line = line.split()
        print(line[0], cipin.get(line[0], 0), line[1], cipin.get(line[1], 0), line[2], line[3])



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

