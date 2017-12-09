#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-07 22:59:49
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import gzip
import json
import re

p = re.compile(r'\(.*same as (.*)\)')

with gzip.open('../dict/kangxi.json.gz') as fd:
    data = json.load(fd)

with open('../dict/Unihan_Readings.json') as fd:
    uni = json.load(fd)

# 音调
#'\u0304\u0301\u030c\u0300'
# for i in data:
#     if 'tyz' in data[i]:
#         tyz = [j.split('|') for j in data[i]['tyz']]
#         # tyz = [j[0] for j in tyz if j[1] == '正體字']
#         # tyz = [j[0] for j in tyz if j[1] == '簡體字']
#         # tyz = [j[0] for j in tyz if j[1] == '同義字']
#         # tyz = [j[0] for j in tyz if j[1] == '異體字']
#         if tyz:
#             print(i, *tyz)
# for i in data:
#     #if '國語發音' not in data[i] and i in uni:
#     if i in uni and 'kDefinition' in uni[i] and 'same' in uni[i]['kDefinition']:
#         print(i, uni[i]['kDefinition'])
#
# for i in uni:
#     if i in uni and 'kDefinition' in uni[i] and 'same' in uni[i]['kDefinition']:
#         print(i, uni[i]['kDefinition'])

for i in data:
    if '國語發音' in data[i]:  # and ('\u0304' in data[i]['國語發音'] or '\u0301' in data[i]['國語發音']  or '\u030c' in data[i]['國語發音']  or '\u0300' in data[i]['國語發音'] ):
        pron = data[i]['國語發音'].split()[0]
        print(f'<char zi="{i}">{pron}</char>')

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

