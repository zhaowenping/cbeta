#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-10-22 14:56:27
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


tt = set()
ss = set()
with open('TSCharacters.txt') as fd:
    for line in fd:
        line = line.strip().split()
        # print(line.split())
        tt.add(line[0])
        for zi in line[1:]:
            ss.add(zi)

xx = tt & ss
tt = tt - xx
ss = ss - xx
#print(tt)
#print(ss)
#print(len(ss & tt))
def tsdect(s0):
    '''判断一段文本是简体还是繁体的概率'''
    s0 = set(s0)
    # 繁体概率
    t = 150 - (len(s0 - tt) * 100 / len(s0))
    # 简体概率
    s = 150 - (len(s0 - ss) * 100 / len(s0))
    return {'t': t, 's': s}

print(tsdect('大佛顶首楞严'))
print(tsdect('轉檔程式'))
print(tsdect('StarDict is the leading cross-platform, open-source dictionary software. '))
print(tsdect('丁福保'))



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

