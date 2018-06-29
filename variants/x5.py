#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-06-20 22:08:40
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import json

with open('../../cipin.json') as fd:
    cipint = json.load(fd)

with open('tw_edu.json') as fd:
    edu = json.load(fd)



result = set()
rr = dict()
with open('variants.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip()
        if not line: continue
        data = line.split()
        c1 = data[0]
        c2 = data[1]
        # c3 = data[2]
        # if c1 in rr:
        #     rr[c1].append(c2)
        # else:
        #     rr[c1] = [c2,]
        rr [c2] = c1
        # result.add((c1, c2))
        # else:
        #     print(c2)

import psycopg2
aa = 0
conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
cur = conn.cursor()
sql = 'select uni, nun, nor, cipin, des  from cb2  where uni is not null order by cipin desc'
cur.execute(sql)
data = cur.fetchall()
for i in data:
    uni = i[0].strip()  # [18:]
    nun = i[1]
    nor = i[2]
    cipin = i[3]
    des = i[4]
    if uni not in rr and cipin > 0:
        print(uni, "U+%X" % ord(uni), cipin)
        aa = aa + 1
        pass
    # elif rr[uni] != nor and nor is not None and cipin > 0:
    #     print(uni, nor, rr[uni], cipint.get(nor, 0), cipint.get(rr[uni], 0))  # , "U+%X" % ord(nor), "U+%X" % ord(rr[uni]))

    # if uni not in result and uni not in result.values():
    #     print(uni, nun, nor, cipin)

conn.commit()
cur.close()
conn.close()

print(aa)

# # result = sorted(list(result), key=lambda x: ord(x[0]))
# rk = sorted(rr.keys(), key=lambda x: ord(x))
#
# for c1 in rk:
#     cc = sorted([i for i in rr[c1]], key=lambda x: ord(x))
#     for c2 in cc:
#         # if c1 in edu and c2 in edu:
#         if c1 != c2:
#             print(c1, c2, "U+%X" % ord(c1), "U+%X" % ord(c2))
#
# print(data)


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

