#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-12-09 10:23:23
from __future__ import unicode_literals, division, absolute_import, print_function

"""
函数库
1. 简体繁体检测
2. 简体繁体转换
3. 注音 phonetic notation
4. 注音格式转换
"""

__all__ = []
__author__ = ""
__version__ = "0.0.1"


import re
import os
import gzip
import json
import time
from functools import reduce




print('调用函数库')

class TSDetect:
    '''简体繁体检测'''
    def __init__(self):

        self.p = re.compile(r'[\u4e00-\u9fa5]')

        self.tt = set()
        self.ss = set()
        # with open('static/TSCharacters.txt') as fd:
        with open('cc/TSCharacters.txt') as fd:
            for line in fd:
                line = line.strip().split()
                # print(line.split())
                self.tt.add(line[0])
                for zi in line[1:]:
                    self.ss.add(zi)

        xx = self.tt & self.ss
        self.tt = self.tt - xx
        self.ss = self.ss - xx

    def detect(self, s0):
        '''判断一段文本是简体还是繁体的概率'''
        s0 = set(s0)
        # 同时是简体繁体的概率
        j = 0
        aa = s0 - self.tt - self.ss
        for i in aa:
            if self.p.match(i):
                j += 1
        # 繁体概率
        t = 100 +  ((j * 50 -len(s0 - self.tt) * 100 )/ len(s0))
        # 简体概率
        s = 100 + ((j * 50 - len(s0 - self.ss) * 100 )/ len(s0))

        confidence = ''
        if t > 50:
            confidence = 't'
        elif s > 50:
            confidence = 's'
        return {'t': t, 's': s, 'confidence': confidence}


def read_menu_file(sutra_list):
    '''读取tab分隔的菜单文件，返回树状字典'''
    menu = dict()

    with open(sutra_list) as fd:
        for line in fd:
            line = line.rstrip()
            # if line.startswith('\t\t\t\t\t'):
            #     print(line)
            if not line.startswith('\t'):
                key1 = line
                menu.update({line:{}})
                continue
            line = line[1:]

            if not line.startswith('\t'):
                key2 = line
                menu[key1].update({line: {}})
                continue
            line = line[1:]

            if not line.startswith('\t'):
                key3 = line
                menu[key1][key2].update({line: {}})
                continue
            line = line[1:]

            if not line.startswith('\t'):
                key4 = line
                menu[key1][key2][key3].update({line: {}})
                continue
            line = line[1:]

            if not line.startswith('\t'):
                key5 = line
                menu[key1][key2][key3][key4].update({line: {}})
                continue
            line = line[1:]

            if not line.startswith('\t'):
                menu[key1][key2][key3][key4][key5].update({line: {}})
                continue
        return menu

def get_all_juan(sutra):
    '''给定经号T01n0002，返回所有排序后的卷['001', '002', ...]'''
    ye = sutra.split('n')[0]
    # 查找第一卷(有些不是从第一卷开始的)
    juan = []
    for path in os.listdir('xml/{ye}'.format(**locals())):
        if path.startswith(sutra):
            print(path)
            juan.append(path.split('_')[1][:-4])
            # juan.append(path)
    juan.sort()
    return juan

# FROM: https://en.wikipedia.org/wiki/International_Alphabet_of_Sanskrit_Transliteration

# FROM: https://en.wikipedia.org/wiki/Harvard-Kyoto
class SA:
    '''梵语字符串类, 可以使用HK转写和iast转写输入, 使用天城体, 悉檀体, 拉丁输出'''
    pass

def hk2iast(str_in, m=1):
    '''hk系统转拉丁梵语, 会有两个结果，分别是t1和t2'''
    x = {'S':'sh',
        'R':'\u1e5bi',      # ṛi
        'RR':'\u1e5b\u012b'}  #   1e5d

    t1 = {'A': '\u0101',    # ā
        'I':'\u012b',
        'U':'\u016b',
        'M':'\u1e43', # 1e43
        'H':'\u1e25',
        'G':'\u1e45',
        'J':'\u00f1',
        'T':'\u1e6d',
        'D':'\u1e0d',
        'N':'\u1e47',
        'L':'\u1eca',   # Ị
        'z':'\u1e61',
        '@':' ',
        }

    t2 = {'A': '\u0101',
        'I':'\u012b',
        'U':'\u016b',
        'M':'\u1e49', # 1e49
        'H':'\u1e25',
        'G':'\u1e45',
        'J':'\u00f1',
        'T':'\u1e6d',
        'D':'\u1e0d',
        'N':'\u1e47',
        'L':'\u1eca',
        'z':'\u1e61',
        '@':' ',
        }

    if m == 1:
        usedt = {ord(k): ord(t1[k]) for k in t1}
    else:
        usedt = {ord(k): ord(t2[k]) for k in t2}
    str_out = str_in.replace('S', 'sh').replace('RR', '\u1e5b\u012b').replace('R', '\u1e5bi')
    str_out = str_out.translate(usedt)
    return str_out

hk2sa = hk2iast

def load_dict():

    # 装入梵英词典, 太大了，暂时不装了
    mwpatten = re.compile(r'(%\{.+?})')
    sa_en = dict()

    # s = time.time()
    # with gzip.open('dict/sa-en.json.gz') as fd:
    #     data = fd.read()
    # data = json.loads(data)
    # sa_en = dict()
    # for key in data:
    #     k = key.replace('1', '').replace("'", '').replace('4', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('-', '').lower()
    #     sa_en.update({k: data[key]})
    #
    # for key in data:
    #     vals = data[key]
    #     res = []
    #     for val in vals:
    #         x = mwpatten.findall(val)
    #         if x:
    #             for ff in x:
    #                 val = val.replace(ff, hk2sa(ff))
    #         res.append(val)
    #     # 不知道以下这两行那个对
    #     sa_en.update({hk2sa(key, 1): res})
    #     sa_en.update({hk2sa(key, 2): res})
    # e = time.time()
    # print('装入梵英词典，用时%s' % (e - s))

    sa_hant = dict()
    # s = time.time()
    # with gzip.open('dict/sa-hant.json.gz') as fd:
    #     data = fd.read()
    # data = json.loads(data)
    # for key in data:
    #     sa_hant.update({key.lower(): data[key]})
    # e = time.time()
    # print('装入梵汉词典，用时%s' % (e - s))

    yat = dict()
    # s = time.time()
    # with gzip.open('dict/yat.json.gz') as fd:
    #     data = fd.read()
    # data = json.loads(data)
    # for key in data:
    #     yat.update({key.lower(): data[key]})
    # for key in data:
    #     vals = data[key]
    #     res = []
    #     for val in vals:
    #         x = mwpatten.findall(val)
    #         if x:
    #             for ff in x:
    #                 v = val.replace(ff, hk2sa(ff))
    #         res.append(v)
    #     yat.update({hk2sa(key, 1): res})
    #     yat.update({hk2sa(key, 2): res})
    # e = time.time()
    # print('装入Yates梵英词典，用时%s' % (e - s))

    s = time.time()
    with gzip.open('dict/kangxi.json.gz') as fd:
        kangxi = json.load(fd)
    e = time.time()
    print('装入康熙字典，用时%s' % (e - s))

    s = time.time()
    with open('dict/Unihan_Readings.json') as fd:
        unihan = json.load(fd)
    e = time.time()
    print('装入Unicode10.0字典，用时%s' % (e - s))

    s = time.time()
    with gzip.open('dict/fk.json.gz') as fd:
        fk = json.load(fd)
    e = time.time()
    print('装入佛光山词典，用时%s' % (e - s))

    s = time.time()
    with gzip.open('dict/dfb.json.gz') as fd:
        dfb = json.load(fd)
    e = time.time()
    print('装入丁福宝词典，用时%s' % (e - s))

    s = time.time()
    with open('dict/ccc.json') as fd:
        ccc = json.load(fd)
    e = time.time()
    print('装入庄春江词典，用时%s' % (e - s))

    s = time.time()
    with open('dict/nvd.json') as fd:
        nvd = json.load(fd)
    e = time.time()
    print('装入南山律学词典，用时%s' % (e - s))

    s = time.time()
    with open('dict/cxy.json') as fd:
        cxy = json.load(fd)
    e = time.time()
    print('装入佛學常見詞彙（陳義孝），用时%s' % (e - s))

    s = time.time()
    with open('dict/ylb.json') as fd:
        ylb = json.load(fd)
    e = time.time()
    print('装入於凌波，用时%s' % (e - s))

    s = time.time()
    with gzip.open('dict/fxcd.json.gz') as fd:
        fxcd = json.load(fd)
    e = time.time()
    print('装入法相詞典，用时%s' % (e - s))

    print('装入于凌波唯识名词白话新解，用时%s' % (e - s))
    return {'kangxi':kangxi, 'unihan':unihan, 'fk':fk, 'dfb': dfb, 'ccc': ccc, 'nvd': nvd, 'cxy': cxy, 'ylb': ylb, 'fxcd': fxcd,
        'sa_hant': sa_hant, 'sa_en': sa_en, 'yat': yat}



def lookinkangxi(word):
    if word in kangxi:
        definition = []
        kxword = kangxi[word]
        if "說文解字" in kxword:
            definition.append(kxword["說文解字"])
        if "康熙字典" in kxword:
            definition.append(kxword["康熙字典"])
        if "宋本廣韻" in kxword:
            definition.append(kxword["宋本廣韻"])
        if definition:
            definition = '|'.join(definition)
        else:
            definition = kxword.get('英文翻譯', '')
        pinyin = kxword.get('國語發音', '')
    return pinyin, definition


def lookinsa(word):
    definition = sa_hant.get(hk2sa(word).lower(), '')
    if definition:
        _from = "文理学院"
        pinyin = "文理学院"
    if not definition:
        # 使用Harvard-Kyoto转写查找字典
        definition = sa_en.get(hk2sa(word), '')
        # 使用缩写查找字典
        if not definition:
            w = word.replace('1', '').replace("'", '').replace('4', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('-', '').lower()
            definition = sa_en.get(w, '')
        if definition:
            definition = '|'.join(definition)
            _from = "威廉梵英词典"
            pinyin = "威廉梵英词典"
    if not definition:
        print(hk2sa(word))
        definition = yat.get(hk2sa(word), '')
        if not definition:
            w = word.replace('-', '').lower()
            definition = yat.get(w, '')
        if definition:
            definition = '|'.join(definition)
            _from = "YAT"
            pinyin = "YAT"


class Search:
    def __init__(self):
        mulu = read_menu_file("static/sutra_sch.lst")
        #pprint.pprint(m['T 大正藏'])
        # d = mulu['T 大正藏']
        def walk(d, result=[]):
            '''遍历目录树'''
            for x in d:
                if not d[x]:
                    result.append(x)
                else:
                    walk(d[x], result)
            return result


        result = walk(mulu)
        result = [i.split(maxsplit=2) for i in result]
        titles = [(i[0], ' '.join((i[1], i[2]))) for i in result]
        # titles 是经号和title的对照表
        # 生成索引表
        self.index = {}
        for i in titles:
            z = 0
            #print(i)
            for j in i[1]:
                if j in self.index:
                    self.index[j].append((i[0], z))
                else:
                    self.index[j] = [(i[0], z),]
                #print(j, i[0], z)
                z += 1
        for i in self.index:
            # print(i)
            v = self.index[i]
            r = dict()
            for j in v:
                if j[0] in r:
                    r[j[0]].append(j[1])
                else:
                    r[j[0]] = [j[1],]
            # pprint.pprint((i, r))
            self.index.update({i: r})
        self.titles = dict(titles)


    def search(self, title):
        # title = opencc.convert(title, config='s2t.json')
        # ( for zi in index)
        a = (set(self.index.get(tt, {}).keys()) for tt in list(title))
        return reduce(lambda x, y: x & y, a)

def main():
    ''''''
    ss = Search()
    title = '成唯识论'
    import opencc
    title = opencc.convert(title, config='s2t.json')
    s = time.time()
    ss.search(title)
    e = time.time()
    print(e-s)
    for idx in ss.search(title):
        print(idx, ss.titles[idx])


def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()


