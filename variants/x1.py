#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-15 21:00:34
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

with open('z.txt') as fd:
    for line in fd:
        line = line.strip()
        if line.startswith('#'): continue
        line = line.split()
        c1 = line[0]
        c2 = line[1]
        print(c1,c2, "U+%X" % ord(c1), "U+%X" % ord(c2))

        # if len(line) == 4:
        #     if dd[0] in edu: # and c2 not in edu:
        #         print(dd[0], dd[1], dd[2], dd[3], "U+%X" % ord(dd[0]), "U+%X" % ord(dd[1]), "U+%X" % ord(dd[2]), "U+%X" % ord(dd[3]))
        #         pass
        #     else:
        #         #print(dd[0], dd[1], dd[2], dd[3], "U+%X" % ord(dd[0]), "U+%X" % ord(dd[1]), "U+%X" % ord(dd[2]), "U+%X" % ord(dd[3]))
        #         pass



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

