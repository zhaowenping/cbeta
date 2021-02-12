#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2021-02-11 17:31:26
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import json

word = 'xx'
a = {
     "query": {
         # "match_phrase": { "orth": nword},  # "content": {"query": sentence, "slop": 1} },
         "match": {"orth":
             {"query": word,
              "operator": "and"
             },  # "content": {"query": sentence, "slop": 1} },
             }
       #  "bool":{
            #  "must": {}
       # }
    },
    "size": 5000,
    "from": 0,
    # "highlight": {
    #     "fields": {
    #         "raw": {

    #         }
    #     }
    # }
    }

print(a)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

