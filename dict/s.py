#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-02-13 20:20:15
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json
import pprint
import gzip

with open('yzzj.json') as fd:
    data = json.load(fd)

#data = data.translate({0x25CB: 0x3007})
# with open('xx.xml', 'w') as fd:
#     fd.write(data)

result = dict()
h = data.pop('header')
result['header'] = h

for k in data:
    # if '■' in k or '◎' in k:
    nk = k.strip()
    if '（' in nk:
        nk, v = nk.split('（', maxsplit=1)
        v = '（' + v + data[k]
        #print(nk, v)
        if nk in result:
            print(k)
        result[nk] = v
        # print('------------------')
    else:
        if nk in result:
            print(k)
        result[nk] = data[k]


# pprint.pprint(result)
print(json.dumps(result,ensure_ascii=False, indent =4))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

