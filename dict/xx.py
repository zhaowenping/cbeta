#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-09-29 22:41:06
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


# with open('ganz.txt', encoding='ascii') as fd:
with open('ganz.txt', 'rb') as fd:
    # data = fd.read()
    for line in fd:
        line = line.strip()# .split(b'\t')
        try:
            line = line.decode('utf8')
        except UnicodeDecodeError as e:
            print(line)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

