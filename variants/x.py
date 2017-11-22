#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-11-22 21:37:36
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json

with open('tw_edu.json') as fd:
    edu = json.load(fd)

with open('xx.json') as fd:
    for line in fd:
        line = line.strip()
        # print(line)
        r = json.loads(line)
        if len(r) == 6:
            if r[0] in edu:
                # print(r[0], r[1], r[2], r[3], r[4], r[5])
                pass
            elif r[1] in edu:
                # print(r[1], r[0], r[2], r[3], r[4], r[5])
                pass
            elif r[2] in edu:
                # print(r[2], r[0], r[1], r[3], r[4], r[5])
                pass
            elif r[3] in edu:
                # print(r[3], r[0], r[1], r[2], r[4], r[5])
                pass
            elif r[4] in edu:
                # print(r[4], r[0], r[1], r[2], r[3], r[5])
                pass
            elif r[5] in edu:
                # print(r[5], r[0], r[1], r[2], r[3], r[4])
                pass
            else:
                # print(a, b, c, d)
                # print(r[0], r[1], r[2], r[3], r[4], r[5])
                pass
        if len(r) == 7:
            if r[0] in edu:
                # print(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
                pass
            elif r[1] in edu:
                # print(r[1], r[0], r[2], r[3], r[4], r[5], r[6])
                pass
            elif r[2] in edu:
                # print(r[2], r[0], r[1], r[3], r[4], r[5], r[6])
                pass
            elif r[3] in edu:
                # print(r[3], r[0], r[1], r[2], r[4], r[5], r[6])
                pass
            elif r[4] in edu:
                # print(r[4], r[0], r[1], r[2], r[3], r[5], r[6])
                pass
            elif r[5] in edu:
                # print(r[5], r[0], r[1], r[2], r[3], r[4], r[6])
                pass
            else:
                # print(a, b, c, d)
                # print(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
                pass
        if len(r) == 9:
            if r[0] in edu:
                print(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8])
                pass
            elif r[1] in edu:
                print(r[1], r[0], r[2], r[3], r[4], r[5], r[6], r[7])
                pass
            elif r[2] in edu:
                print(r[2], r[0], r[1], r[3], r[4], r[5], r[6], r[7])
                pass
            elif r[3] in edu:
                print(r[3], r[0], r[1], r[2], r[4], r[5], r[6], r[7])
                pass
            elif r[4] in edu:
                print(r[4], r[0], r[1], r[2], r[3], r[5], r[6], r[7])
                pass
            elif r[5] in edu:
                print(r[5], r[0], r[1], r[2], r[3], r[4], r[6], r[7])
                pass
            else:
                # print(a, b, c, d)
                # print(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
                pass




def main():
    ''''''





def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

