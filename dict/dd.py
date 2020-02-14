#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-02-13 19:58:44
from __future__ import unicode_literals, division, absolute_import, print_function

"""
替换组字式为正字
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import re
import json
import gzip

p = re.compile(r'\[.*?\]')

with open('d3.json') as fd:
    d2 = json.load(fd)

with open('d3.txt') as fd:
    for line in fd:
        line = line.strip()
        if not line : continue
        kv = line.split()
        if len(kv) != 2:
            print(kv)
            continue
        d2.update({kv[0]:[None,kv[1]]})

# with open('ddbc.nanshanlu.tei.p5.xml') as fd:
#with open('ddbc.soothill-hodous.tei.p5.xml') as fd:
# with open('dharmaraksa.ddbc.tei.p5.xml') as fd:  TODO
# with open('kumarajiva.ddbc.tei.p5.xml') as fd:
#with open('lokaksema.xml') as fd:
#with open('bkqs.json') as fd:
#with open('dzdl.gls.txt') as fd:
# with open('fk.json') as fd:
#with open('fxcd.json') as fd:
#with open('fymyj.json') as fd:
#with open('ldms.json') as fd:
#with open('wdhy.json') as fd:
with open('yzzj.json') as fd:
    data = fd.read()

# data = data.translate({0x25CB:ord('〇')})
# with gzip.open('../cbeta/dict/fk.json.gz') as fd:
#     data = fd.read().decode('utf8')

for des in d2:
    if d2[des][1]:
        data = data.replace(des, d2[des][1])
    elif d2[des][0]:
        print('000000000', des, d2[des])
        data = data.replace(des, d2[des][0])
    else:
        print('222222222', des, d2[des])

with open('dfb.xml', 'w') as fd:
    fd.write(data)
with open('dfb.xml') as fd:
    data = fd.read()

xx = p.findall(data)
result = dict()
for zi in xx:
    if zi in result:
        result[zi] = result[zi] + 1
    else:
        result[zi] = 1

# for zi in result:
#     if zi not in d2.keys():
#         print(zi)
import pprint
pprint.pprint(result)
#print(xx)
#print(set(xx))
#print(len(set(xx)))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

