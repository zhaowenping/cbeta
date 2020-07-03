#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-07-02 21:12:43
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import re, json

with open('composition.json') as fd:
    desc = json.load(fd)

# pattern = '|'.join(['\[%s\]' % k[1:-1].replace('*', '\*').replace('?', '\?')  for k in desc.keys()])
for ctx in desc:
    #if not re.findall(r'\[.*?\]', ctx):
    if not re.findall(r'\[[\w*()+@?、/\-]*\]', ctx):
        print(ctx, desc[ctx])

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

