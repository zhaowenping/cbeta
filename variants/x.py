#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-11-22 20:13:04
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json

with open('tw_edu.json') as fd:
    edu = json.load(fd)

with open('kSpecializedSemanticVariant.json') as fd:
    for line in fd:
        a, b, c, d = line.strip().split()
        if a in edu:
            print(a, b, c, d)
            pass
        elif b in edu:
            print(b,a, d, c)
            pass
        else:
            # print(a, b, c, d)
            pass




def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

