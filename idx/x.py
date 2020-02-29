#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-02-29 05:00:54
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re

# T02n0099_001#p0001a06
p = re.compile(r'<li><cblink href="XML/T/T02/([_\w#]+)">([-\d]+)<')

i = 0
with open('T0099.xml') as fd:
    for line in fd:
        line = line.strip()
        if '<ol>' in line:
            i = i+1
        x = p.findall(line)
        if x:
            print(x[0][1], x[0][0])


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

