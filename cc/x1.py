#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-14 10:29:45
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import opencc
import time

ts = dict()
with open('TSCharacters.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip().split()
        # ts[line[0]] = line[1:][0]
        ts[ord(line[0])] = ord(line[1:][0])
        if(len(line[1:])>1):
            print(line)
        #tt.add(line[0])
        #for zi in line[1:]:
        #    ss.add(zi)




def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

