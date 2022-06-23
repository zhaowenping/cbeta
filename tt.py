#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2022-06-22 21:17:17
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re

def python_unescape(ctx):
    '''替换python字样转义字符串为正常汉字'''
    #for ch in re.findall(r'(?:[^\\]|^)(\\u[a-fA-F0-9]{4})', ctx):
    for ch in re.findall(r'(\\u[a-fA-F0-9]{4})', ctx):
        ctx = ctx.replace(ch, chr(int(ch[-4:], 16)))
    #for ch in re.findall(r'(?:[^\\]|^)(\\U[a-fA-F0-9]{8})', ctx):
    for ch in re.findall(r'(\\U[a-fA-F0-9]{8})', ctx):
        ctx = ctx.replace(ch, chr(int(ch[-8:], 16)))
    # ctx = ctx.replace(r'\\\\', r'\\')

    return ctx

ctx = r'\u6211\u672c\u662f\u663e\u8d6b\u4e16\u5bb6\u7684\u5965\u7279\u66fc\uff0c\u5374\u88ab\u8be1\u8ba1\u591a\u7aef\u7684\u602a\u517d\u6240\u5bb3\uff01\u5965\u7279\u66fc\u5bb6\u65cf\u5f03\u6211\uff01\u5965\u7279\u4e4b\u7236\u9010\u6211\uff01\u751a\u81f3\u65ad\u6211\u4f3d\u9a6c\u5c04\u7ebf\uff01\u91cd\u751f'
xx = python_unescape(ctx)
print (xx)



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

