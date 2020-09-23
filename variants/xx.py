#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-09-22 20:54:18
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


def split(ctx, fn=lambda x:x):
    '''将字符串按照ids序列分隔为数组。遇到ids序列的时候，使用fn处理，返回全部数组。'''
    result = []
    counter = 0
    rr = []
    for ch in ctx:
        if ch in '⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻':
            if counter == 0:
                counter = 2
            else:
                counter = counter + 1
            rr.append(ch)
        elif ch in '⿲⿳':
            if counter == 0:
                counter = 3
            else:
                counter = counter + 2
            rr.append(ch)
        else:
            if counter == 0:
                result.append(ch)
            else:
                if counter != 0:
                    counter = counter - 1
                    rr.append(ch)
                if counter == 0:
                    result.append(''.join(rr))
                    rr = []
    return result


def split(ctx, fn=lambda x:x):
    '''将字符串按照ids序列分隔为数组。遇到ids序列的时候，使用fn处理，返回全部数组。'''
    counter = 0
    tmp = []
    for ch in ctx:
        if counter == 0:
            if tmp and ch in '↷↹⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻⿲⿳':
                yield ''.join(tmp)
                tmp = []
            if ch in '↷↹':
                counter = 1
            if ch in '⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻':
                counter = 2
            if ch in '⿲⿳':
                counter = 3
            tmp.append(ch)
        else:
            tmp.append(ch)
            if ch in '↷↹':
                pass
            if ch in '⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻':
                counter = counter + 1
            elif ch in '⿲⿳':
                counter = counter + 2
            else:
                counter = counter - 1
                if counter == 0:
                    yield ''.join(fn(tmp))
                    tmp= []
    yield ''.join(tmp)


def ids_split(ctx, fn=lambda x:x):
    '''将字符串按照ids序列分隔为数组。遇到ids序列的时候，使用fn处理，返回全部数组。'''
    tmp = []
    counter = 0
    for ch in ctx:
        if counter == 0:
            if tmp and ch in '↷↹⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻⿲⿳':
                yield ''.join(tmp)
                tmp = []
            if ch in '↷↹':
                counter = 1
            elif ch in '⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻':
                counter = 2
            elif ch in '⿲⿳':
                counter = 3
            tmp.append(ch)
        else:
            tmp.append(ch)
            if ch in '↷↹':
                pass
            elif ch in '⿰⿱⿴⿵⿶⿷⿸⿹⿺⿻':
                counter = counter + 1
            elif ch in '⿲⿳':
                counter = counter + 2
            else:
                counter = counter - 1
                if counter == 0:
                    yield fn(''.join(tmp))
                    tmp= []
    yield ''.join(tmp)


print(list(split('⿰我很好⿰人⿲尔号马啊')))
for i in split('⿰我很好⿰人⿲尔号马啊'):
    print(i)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

