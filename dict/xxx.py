#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-09-30 18:03:07
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

import json

with open('tamil.json') as fd:
    data = fd.read()

data = json.loads(data)
print(len(data))
for k in data:
    print(k)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

