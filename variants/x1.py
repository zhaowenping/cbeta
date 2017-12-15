#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-15 20:28:44
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json

with open('tw_edu.json') as fd:
    edu = json.load(fd)

# print(len(edu))

with open('variants.txt') as fd:
    for line in fd:
        line = line.strip()
        if line.startswith('#'): continue
        line = line.split('›〔')
        c1 = line[0][0]

        if len(line) != 2:
            continue
        #print(line)
        c2 = line[1]
        if '、' in c2:
            c2 = [i[0] for i in c2.split('、')]
            dd = c1, * c2
        else:
            c2 = c2[0]
            dd = c1, c2
        # print(c1, c2)
        # if len(dd) == 2:
        #     if c1 not in edu and c2 in edu:
        #         # print(dd[0], dd[1], "U+%X" % ord(dd[0]), "U+%X" % ord(dd[1]))
        #         print(dd[1], dd[0], "U+%X" % ord(dd[1]), "U+%X" % ord(dd[0]))
        if len(dd) == 4:
            if dd[0] in edu: # and c2 not in edu:
                print(dd[0], dd[1], dd[2], dd[3], "U+%X" % ord(dd[0]), "U+%X" % ord(dd[1]), "U+%X" % ord(dd[2]), "U+%X" % ord(dd[3]))
                pass
            else:
                #print(dd[0], dd[1], dd[2], dd[3], "U+%X" % ord(dd[0]), "U+%X" % ord(dd[1]), "U+%X" % ord(dd[2]), "U+%X" % ord(dd[3]))
                pass



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

