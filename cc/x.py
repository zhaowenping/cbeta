#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-02-01 22:21:48
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


with open('TSCharacters.txt') as fd:
    for line in fd:
        line = line.strip().split()
        if len(line) == 2:
            c1, c2 = line
            print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))
        elif len(line) == 3:
            c1, c2, c3 = line
            print(c1, c2, c3, "U+%X" % ord(c1), "U+%X" % ord(c2))
        else:
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', line)




def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

