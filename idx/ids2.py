#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-06-02 07:15:01
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re

ids_dict = dict()
with open('ids.txt') as fd:
    for line in fd:
        line = line.strip().split()
        ids_dict[line[2]] = line[1]

ids_pattern = sorted(ids_dict.keys(), key=len, reverse=True)
print('⿰言羊' in ids_pattern)

def rm_ids(ctx):
    # 替换unicode ids形式
    ids = False
    for ch in ctx:
        if 0x2FF0 <= ord(ch) <= 0x2FFB:
            ids = True
            break
    if not ids:
        return ctx

    for ids in ids_pattern:
        if ids in ctx:
            ctx = ctx.replace(ids, ids_dict.get(ids, ' '))

    return ctx

print(rm_ids('言辭⿰言羊j'))
print(rm_ids('⿰山叵⿰山我'))

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

