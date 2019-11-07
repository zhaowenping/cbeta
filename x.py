#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-11-07 02:48:28
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import re

sch_db = []
with open("static/sutra_sch.lst") as fd:
    for line in fd:
        if 'n' in line:
            line = line.strip().split()[0]
            sch_db.append(line)


# 模式1: t1000, t1000_001, T01n0001, T01n0001_001, T01n0001_p0001a01
# 模式2: T01,no.1,p.1a1
# CBETA 2019.Q2, Y25, no. 25, p. 411a5-7
# 模式0: 100, '100,3'
jinghaopatten = re.compile(r'([a-zA-Z]+)(?:(\d\d)n)?(\d{4})(?:_(\d{3}))?(?:[_#](p\d{4}[abc]\d\d))?')
jinghaopatten2 = re.compile(r'([a-zA-Z]+)(\d\d),\s*no\.\s*(\d+),\s*p\.\s*(\d+)([abc])(\d+)')
def make_url(title):
    print(title, end=': ')
    # j1, j2,   j3,  j4, j5
    #  T, 01, 0001, 001, p0001a01
    if title.isdigit():
        j1,j2,j4,j5 = 'T', '', '', ''
        j3 = '{:04}'.format(int(title))
    else:
        jinghao = jinghaopatten.findall(title)
        if jinghao:
            j1,j2,j3,j4,j5 = jinghao[0]
        else:
            jinghao = jinghaopatten2.findall(title)
            if not jinghao:
                return None
            j4 = ''
            j1,j2,j3,j5,j6,j7 = jinghao[0]
            j3 = '{:04}'.format(int(j3))
            j5 = 'p{:04}{}{:02}'.format(int(j5), j6, int(j7))

    j1 = j1.upper()
    # 查找册数 TODO
    if not j2:
        for line in sch_db:
            if j1 in line and j3 in line:
                j2 = line.split('n')[0][len(j1):]
                break
    if not j2:
        return None
    # 查找卷数 TODO
    if not j4:
        pass
    # 如果有锚就添加锚
    if j5:
        url = f'{j1}{j2}n{j3}_{j4}.xml#{j5}'
    else:
        url = f'{j1}{j2}n{j3}_{j4}.xml'
    return url

#print(j1,j2,j3,j4,j5)
#print(url)
print(make_url('10'))
print(make_url('T01,no.1,p.1a1'))
print(make_url('你好'))
print(make_url('t1000'))
print(make_url('GA1000_001'))
print(make_url('T01n0001'))
print(make_url('T01n0001_001'))
print(make_url('T01n0001_p0001a01'))
print(make_url('CBETA 2019.Q2, Y25, no. 25, p. 411a5-7'))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

