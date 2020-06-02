#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-06-02 06:37:12
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

import pprint
print(re.compile('|'.join(sorted(ids_dict.keys(), key=len, reverse=True))))
pprint.pprint(ids_dict)
def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

