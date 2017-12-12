#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-11 18:38:37
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
        line = line.strip().split()
        # ts[line[0]] = line[1:][0]
        ts[ord(line[0])] = ord(line[1:][0])
        if(len(line[1:])>1):
            print(line)
        #tt.add(line[0])
        #for zi in line[1:]:
        #    ss.add(zi)


# print(ts)
# str_out.translate(usedt)
with open('../../xml/B31/B31n0170_003.xml') as fd:
    content = fd.read()

s = time.time()
content = opencc.convert(content, config='t2s.json')
e = time.time()
cc = e - s
s = time.time()
content = content.translate(ts)
e = time.time()
print(cc, e-s)



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

