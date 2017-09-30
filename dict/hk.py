#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-09-30 17:59:44
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


x = {'A': '\u0101',
        'I':'\u012b',
        'U':'\u016b',
        'R':'\u1e5bi',
        'RR':'\u1e5b\u012b',
        'lR':'l\u1e5bi',
        'lRR':'l\u1e5b\u012b',
        'M':'\u1e43', # 1e49
        'H':'\u1e25',
        'G':'\u1e45',
        'J':'\u00f1',
        'T':'\u1e6d',
        'Th':'\u1e6dh',
        'D':'\u1e0d',
        'Dh':'\u1e0dh',
        'N':'\u1e47',
        'L':'\u1eca',
        'z':'\u1e61',
        'S':'sh',
        }

def sa2hk(str_in):
    '''拉丁梵语转hk系统'''

def hk2sa(str_in):
    '''hk系统转拉丁梵语, 会有两个结果，分别是t1和t2'''
    x = {'S':'sh',
        'R':'\u1e5bi',
        'RR':'\u1e5b\u012b'}

    t1 = {'A': '\u0101',
        'I':'\u012b',
        'U':'\u016b',
        'M':'\u1e43', # 1e49
        'H':'\u1e25',
        'G':'\u1e45',
        'J':'\u00f1',
        'T':'\u1e6d',
        'D':'\u1e0d',
        'N':'\u1e47',
        'L':'\u1eca',
        'z':'\u1e61',
        }

    t2 = {'A': '\u0101',
        'I':'\u012b',
        'U':'\u016b',
        'M':'\u1e49', # 1e49
        'H':'\u1e25',
        'G':'\u1e45',
        'J':'\u00f1',
        'T':'\u1e6d',
        'D':'\u1e0d',
        'N':'\u1e47',
        'L':'\u1eca',
        'z':'\u1e61',
        }

    t1 = {ord(k): ord(t1[k]) for k in t1}
    t2 = {ord(k): ord(t2[k]) for k in t2}
    str_out = str_in.replace('S', 'sh').replace('RR', '\u1e5b\u012b').replace('R', '\u1e5bi')
    str_out = str_out.translate(t1)
    return str_out

print(hk2sa('jambudvIpa'))
import pprint

#pprint.pprint(x)
def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

