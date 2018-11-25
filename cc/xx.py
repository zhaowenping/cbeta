#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-11-25 12:17:41
from __future__ import unicode_literals, division, absolute_import, print_function

"""
规范化繁体转简体字库
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


result = []
with open('TSCharacters.txt') as fd:
    for line in fd:
        line = line.strip()
        if line.startswith('#'):
            continue
        line = line.split()
        if len(line) == 2 and line[0] == line[1]:
            pass
        elif len(line) == 2:
            result.append(line)
            pass
        elif len(line) > 2:
            # print(line)
            pass

result = sorted(result, key=lambda x :ord(x[0]))
for line in result:
    a, b = line
    # if ord(a) < 0x20000 and ord(b) > 0x20000:
    #$ if ord(b) > 0x20000:
    #$     print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), 1)
    #$ else:
    #$     print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), 0)
    # if not (ord(a) < 0x20000 and ord(b) > 0x20000):
    if not (ord(b) < 0x4E00 or ord(b) > 0x20000):
        print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), 0)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

