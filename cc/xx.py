#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-01-21 16:11:31
from __future__ import unicode_literals, division, absolute_import, print_function

"""
规范化繁体转简体字库
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


cipin = dict()
with open('../../cp.txt') as fd:
    for line in fd:
        line = line.strip().split()
        # line[2] = int(line[2])
        cipin[line[0]] = line[2]

result = []
with open('TSCharacters.txt') as fd:
    for line in fd:
        line = line.strip()
        if line.startswith('#'):
            continue
        line = line.split()
        if len(line) == 2 and line[0] == line[1]:
            a = line[0]
            b = line[1]
            # print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), 0)
            result.append(line)
            pass
        elif len(line) == 2:
            result.append(line)
            pass
        elif len(line) > 2:
            # print(line)
            pass

result = sorted(result, key=lambda x :ord(x[0]))
rr = []
for line in result:
    a, b = line
    # if ord(a) < 0x20000 and ord(b) > 0x20000:
    #$ if ord(b) > 0x20000:
    #$     print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), 1)
    #$ else:
    #$     print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), 0)
    # if not (ord(a) < 0x20000 and ord(b) > 0x20000):
    if not (ord(b) < 0x4E00 or ord(b) > 0x9FAC):
        # print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), cipin.get(a, 0), 0)
        rr.append([a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), cipin.get(a, 0), 0])
    else:
        # print(a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), cipin.get(a, 0), 1)
        rr.append([a, b, 'U+%X' % ord(a), 'U+%X' % ord(b), cipin.get(a, 0), 1])

rr = sorted(rr, key=lambda x :int(x[4]))[::-1]
for zi in rr:
    print(*zi)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

