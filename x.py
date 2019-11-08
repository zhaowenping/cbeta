#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-11-07 18:43:25
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import os
import re

def get_all_juan(number):
    '''给定经号T01n0002，返回所有排序后的卷['001', '002', ...]
    返回值是一个数组，如果没有找到则返回空的数组'''
    book, sutra = number.split('n')
    # 查找第一卷(有些不是从第一卷开始的)
    juan = []
    if not os.path.exists(f'../xml/{book}'):
        return None
    for path in os.listdir(f'../xml/{book}'):
        if path.startswith(number):
            juan.append(path.split('_')[1][:-4])
    juan.sort(key=lambda x: int(re.sub(r'[a-zA-Z]*', '', f'{x:0<5}'), 16))
    return juan

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
jinghaopatten0 = re.compile(r'([a-zA-Z]{1,2})?(\d+)\D+(\d+)')
jinghaopatten = re.compile(r'([a-zA-Z]{1,2})(?:(\d\d)n)?(\d{4})(?:_(\d{3}))?(?:[_#](p\d{4}[abc]\d\d))?')
jinghaopatten2 = re.compile(r'([a-zA-Z]{1,2})(\d\d),\s*no\.\s*(\d+),\s*p\.\s*(\d+)([abc])(\d+)')
def make_url(title):
    print(title, end=': ')
    j1, j2, j3, j4, j5 = 'T', '', '', '', ''
    # j1, j2,   j3,  j4, j5
    #  T, 01, 0001, 001, p0001a01
    found = False
    if title.isdigit():
        j3 = '{:04}'.format(int(title))
        found = True

    if not found:
        jinghao = jinghaopatten.findall(title)
        if jinghao:
            j1,j2,j3,j4,j5 = jinghao[0]
            found = True

    if not found:
        jinghao = jinghaopatten2.findall(title)
        # print('XXXX', jinghao)
        if jinghao:
            j1,j2,j3,j5,j6,j7 = jinghao[0]
            j3 = '{:04}'.format(int(j3))
            j5 = 'p{:04}{}{:02}'.format(int(j5), j6, int(j7))
            found = True

    if not found:
        jinghao = jinghaopatten0.findall(title)
        if jinghao:
            j1,j3,j4 = jinghao[0]
            j1 = j1 if j1 else 'T'
            found = True

    if not found:
            return None

    j1 = j1.upper()
    j3 = '{:04}'.format(int(j3))
    # 查找册数
    if not j2:
        for line in sch_db:
            if j1 in line and j3 in line:
                j2 = line.split('n')[0][len(j1):]
                break
    if not j2:
        return None

    # 查找卷数
    if not j4:
        j4 = get_all_juan(f'{j1}{j2}n{j3}')
        if j4:
            j4 = j4[0]

    if not j4:
        return None

    j4 = '{:03}'.format(int(j4))
    # 如果有锚就添加锚
    if j5:
        url = f'xml/{j1}{j2}/{j1}{j2}n{j3}_{j4}.xml#{j5}'
    else:
        url = f'xml/{j1}{j2}/{j1}{j2}n{j3}_{j4}.xml'
    return url



#print(j1,j2,j3,j4,j5)

#print(url)
# print(make_url('10'))
# print(make_url('T01,no.1,p.1a1'))
# print(make_url('你好'))
# print(make_url('t1000'))
# print(make_url('GA1000_001'))
# print(make_url('T01n0001'))
# print(make_url('T01n0001_001'))
# print(make_url('T01n0001_p0001a01'))
print(make_url('CBETA 2019.Q2, Y25, no. 25, p. 411a5-7'))
print(make_url('CBETA 2019.Q3, T03, no. 158, p. 276b21-25'))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

