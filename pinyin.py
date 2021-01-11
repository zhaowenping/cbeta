#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-12-31 05:59:39
from __future__ import unicode_literals, division, absolute_import, print_function

"""
处理有关拼音的各种函数和类
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


# 缺了於的一声?

xx = {"ā":  "a1",
"á":  "a2",
"ǎ":  "a3",
"à":  "a4",
"ō":  "o1",
"ó":  "o2",
"ǒ":  "o3",
"ò":  "o4",
"ē":  "e1",
"é":  "e2",
"ě":  "e3",
"è":  "e4",
"ī":  "i1",
"í":  "i2",
"ǐ":  "i3",
"ì":  "i4",
"ū":  "u1",
"ú":  "u2",
"ǔ":  "u3",
"ù":  "u4",
"ü":  "v0",
"ǘ":  "v2",
"ǚ":  "v3",
"ǜ":  "v4",
"ń":  "n2",
"ḿ":   "m2"}

# 两种不同拼音写法的转换
for zi in xx:
    print(zi, '%04X' % ord(zi), xx[zi])


def main():
    ''''''

def test():
    ''''''
if __name__ == "__main__":
    # main()
    test()

