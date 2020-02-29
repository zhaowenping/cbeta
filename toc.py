#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-02-28 20:41:00
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re

p = re.compile(r'<tree text="(.*?)" action="cscd/(.*?).xml"')

t = 's0305t.tik.toc'
with open(f'../pali/toc3/{t}.xml') as fd:
    for line in fd:
        line = line.strip()
        if not line: continue
        if 'encoding' in line: continue
        r = p.findall(line)
        if not r:
            print(line)
        else:
            print(' '.join((r[0][1], r[0][0])))

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

