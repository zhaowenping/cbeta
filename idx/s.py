#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-02-14 23:09:49
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


with open('z.txt') as fd:
    for line in fd:
        key, val = line.strip().split('|')
        val = val.split()[-1].split('、')[-1]
        # print(key, val)
        with open('../static/sutra_sch.lst') as fd2:
            for line2 in fd2:
                if key.split('_')[0] in line2:
                    val2 = line2.strip().split(maxsplit=2)
                    # print(line2)
                    val = val2[1] + '\u00b7' + val + ' ' + val2[2]
                    print(key, val)  #, line2.split())
                    break

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

