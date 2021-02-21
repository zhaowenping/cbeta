#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2021-02-20 07:15:34
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re

result = dict()
#with open('mochidic.txt') as fd:
#with open('odadic.txt') as fd:
with open('zendic.txt') as fd:
    for line in fd:
        x = re.findall(r'&.*?;', line)
        if x:
            for i in x:
                if i in result:
                    result[i] += 1
                else:
                    result[i] = 1
for k in result:
    print(k, result[k])



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

