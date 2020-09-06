#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-09-05 20:27:33
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"

t = '''
                    <tr class="%s">
                        <td>
                            %d
                        </td>
                        <td>
                            %s
                        </td>
                        <td>
                           %s
                        </td>
                        <td>
                            Approved
                        </td>
                    </tr>
'''
txt = ['', 'success', 'error', 'info', 'warning']
with open('error.txt') as fd:
    i = 0
    for line in fd:
        line = line.split()
        i += 1
        td4 = line[0]
        td3 = line[1]
        print(t % (txt[i%5], i, td3, td4))


def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

