#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-02-12 00:57:36
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json
import pprint

with open('szfsb.json') as fd:
    data = json.load(fd)

result = dict()
h = data.pop('header')
result['header'] = h

for k in data:
    if len(data[k]) != 1:
        print(k)
    result[k] = '\n'.join(i.strip() for i in data[k])

# pprint.pprint(result)
# print(json.dumps(result,ensure_ascii=False, indent =4))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

