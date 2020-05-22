#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-05-22 03:46:17
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re
import json

with open('dict/desc.json') as fd:
    desc = json.load(fd)

def rm_com(ctx):
    # 删除组字式
    # pattern = '|'.join(['\[%s\]' % k[1:-1].replace('*', '\*').replace('?', '\?')  for k in desc.keys()])
    for com in re.findall(r'\[.*?\]', ctx):
        if com in desc:
            ctx = ctx.replace(com, desc[com])
    return ctx

def rm_com2(ctx):
    # 删除组字式
    # pattern = '|'.join(['\[%s\]' % k[1:-1].replace('*', '\*').replace('?', '\?')  for k in desc.keys()])
    com1 = [desc.get(cc, ' ') for cc in re.findall(r'\[.*?\]', ctx)]
    com2 = re.split(r'\[.*?\]', ctx)

    return ctx

print(rm_com('爾推之𨿽𡮢變[厂@已]𣅜未[幾-(戈@人)+(弋@ㄅ)]而復正'))
print(re.findall(r'\[.*?\]', '之道其大僃矣周道將[褒-保+(共-八)]則有孔'))
print(rm_com('之道其大僃矣周道將[褒-保+(共-八)]則有孔'))

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

