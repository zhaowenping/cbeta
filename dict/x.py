#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-09-26 15:56:35
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import re
import psycopg2

p = re.compile(r"\[.*?\]")

result = set()
with open('fk.json') as fd:
    for line in fd:
        line = line.strip()
        r = p.findall(line)
        if r:
            for word in r:
                result.add(word)


conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
cur = conn.cursor()

for word in result:
   #  print(word)
# cur.execute('select * from cb where position(%s in des)>0 or position(%s in name)>0', (q, q))
    # cur.execute('select * from cb where des = %s', (word, ))
    cur.execute('select * from cb where des = %s and (nor is not null or val is not null or nun is not null)', (word, ))
#cur.execute('select * from cb where nor = %s or val = %s or position(%s in des)>0', (q, q, q))
#cur.execute('select * from cb where nor is null or val is null')
    data = cur.fetchone()
    if data:
        # print(data)
        result = []
        #     print(i)
        name = data[0]
        nor =  data[1]
        val =  data[2]
        des =  data[3]
        uni =  data[4]
        pua =  data[5]
        tag =  data[6]
        nun =  data[7]
        x = nor or val
        result.append((nor, val, des, uni, nun))
        print(word, x, result)

conn.commit()
cur.close()
conn.close()


# {'[女*它]': '𡛥',
#         }

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

