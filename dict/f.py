#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-03-02 21:46:27
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"
import json
import gzip
import re
import pprint

with gzip.open('fxcd.json.gz') as fd:
    data = json.load(fd)
header = data.pop('header', {})
#fxcd = [(item, re.split(r'\n *', data[item])[1:]) for item in data]
fxcd = [(item, '\n'.join([c.strip() for c in re.split(r'\n *', data[item])])) for item in data]
total = len(fxcd)
# pprint.pprint(fxcd)

result = dict()
for i in fxcd:
    result[i[0]] = i[1]

print(json.dumps(result, ensure_ascii=False, indent =4))



def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

