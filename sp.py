#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-11-09 16:49:13
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

with open('sp.txt') as fd:
    data = set(fd.read())

data.discard('\n')
data.discard('\t')
data.discard('#')
data.discard(' ')
print(data)
# with open('static/sutra_sch.lst') as fd:
with open('t.txt') as fd:
    for line in fd:
        line = line.strip()
        for zi in line:
            if zi in data and '念' in line:
                line = line.replace(zi, f"\033[0;31;40m{zi}\033[0m")
                print(line)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

