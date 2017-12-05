#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-05 23:21:25
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import gzip
import json

with gzip.open('../dict/kangxi.json.gz') as fd:
    data = json.load(fd)

for i in data:
    if 'tyz' in data[i]:
        tyz = [j.split('|') for j in data[i]['tyz']]
        # tyz = [j[0] for j in tyz if j[1] == '正體字']
        # tyz = [j[0] for j in tyz if j[1] == '簡體字']
        # tyz = [j[0] for j in tyz if j[1] == '同義字']
        tyz = [j[0] for j in tyz if j[1] == '異體字']
        if tyz:
            print(i, *tyz)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

