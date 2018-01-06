#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-01-06 15:41:09
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
import copy
import gzip
import json
import time
from functools import reduce
import requests


print('调用函数库')

class TSDetect:
    '''简体繁体检测'''
    def __init__(self):

        self.p = re.compile(r'[\u4e00-\u9fa5]')

        # 纯繁体字集合
        self.tt = set()
        # 纯简体字集合
        self.ss = set()
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
        '''粗略判断一段文本是简体还是繁体的概率'''
        if len(s0) == 0:
            return {'t': 50, 's': 50, 'confidence': ''}

        s0 = set(s0)
        # 同时是简体繁体的可能性
        j = sum(1 for i in (s0 - self.tt - self.ss) if self.p.match(i))
        # 繁体可能性
        t = 100 + ((j * 50 - len(s0 - self.tt) * 100 )/ len(s0))
        # 简体可能性
        s = 100 + ((j * 50 - len(s0 - self.ss) * 100 )/ len(s0))

        confidence = ''
        if t > 50:
            confidence = 't'
        elif s > 50:
            confidence = 's'
        return {'t': t, 's': s, 'confidence': confidence}

TSDinst = TSDetect()

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

def hk2iast(str_in):
    '''hk哈佛-京都系统转IAST梵语'''
    x = {'S':'sh',
        'RR':'\u1e5b\u012b'}  #   1e5d
        # 'RR':'\u1e5d'}     # 1e5d
        # 'lR':'\u1eca'}     # 1e5d
        # 'lRR':'\u1e39'}     # 1e5d

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
        'R':'\u1e5b',      # ṛ
        'S':'\u1e63',      #
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

    usedt = {ord(k): ord(t1[k]) for k in t1}
    str_out = str_in.replace('RR', '\u1e5d').replace('lR', '\u1eca').replace('lRR', '\u1e39')
    str_out = str_out.translate(usedt)
    return str_out

hk2sa = hk2iast

def load_dict(dictionary=None):

    # 词典列表
    dicts = {'fk': ('佛光山', 'fk.json.gz'), 'dfb': ('丁福保', 'dfb.json.gz'), 'ccc': ('庄春江', 'ccc.json'), 'fxcd': ('法相詞典', 'fxcd.json.gz'),
            'nvd': ('南山律学词典', 'nvd.json'), 'cxy': ('佛學常見詞彙（陳義孝）', 'cxy.json'), 'ylb': ('唯识名词白话新解', 'ylb.json'),
            'szfs': ('三藏法数', 'szfs.json'), 'fymyj': ('翻譯名義集', 'fymyj.json'), 'wdhy': ('五燈會元', 'wdhy.json.gz'), 'yzzj': ('閱藏知津', 'yzzj.json.gz'),
            'ldms': ('歷代名僧辭典', 'ldms.json.gz'), 'syfy': ('俗語佛源', 'syfy.json.gz'), 'bkqs': ('中华佛教百科全书','bkqs.json.gz')}

    aio = dict()

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
    yield ('sa_en', sa_en)

    sa_hant = dict()
    # s = time.time()
    # with gzip.open('dict/sa-hant.json.gz') as fd:
    #     data = fd.read()
    # data = json.loads(data)
    # for key in data:
    #     sa_hant.update({key.lower(): data[key]})
    # e = time.time()
    # print('装入梵汉词典，用时%s' % (e - s))
    yield ('sa_hant', sa_hant)

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
    yield ('yat', yat)

    s = time.time()
    with gzip.open('dict/kangxi.json.gz') as fd:
        kangxi = json.load(fd)
    e = time.time()
    print('装入康熙字典，用时%s' % (e - s))
    yield ('kangxi', kangxi)

    s = time.time()
    with open('dict/Unihan_Readings.json') as fd:
        unihan = json.load(fd)
    e = time.time()
    print('装入Unicode10.0字典，用时%s' % (e - s))
    yield ('unihan', unihan)

    for k in dicts:
        s = time.time()
        path = f'dict/{dicts[k][1]}'
        if not os.path.exists(path):
            continue

        if path.endswith('gz'):
            with gzip.open(path) as fd:
                v = json.load(fd)
        else:
            with open(path) as fd:
                v = json.load(fd)
        # for k1 in v:
        #     if k1 in aio:
        #         aio[k1].update({dicts[k][0]: v[k1]})
        #     #     aio[k1].append()
        #     else:
        #         aio[k1] = {dicts[k][0]: v[k1]}
        e = time.time()
        print('装入%s，用时%s' % (dicts[k][0], e - s))
        yield (k, v)

    yield ('aio', aio)

    # return {'kangxi':kangxi, 'unihan':unihan,
    #         'fk':fk, 'dfb': dfb, 'ccc': ccc, 'nvd': nvd, 'cxy': cxy, 'ylb': ylb, 'fxcd': fxcd,
    #         'szfs': szfs, 'fymyj': fymyj,
    #     'sa_hant': sa_hant, 'sa_en': sa_en, 'yat': yat}



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


# 装入各种词典
dd = dict(load_dict())
sa_hant = dd['sa_hant']
sa_en = dd['sa_en']
yat = dd['yat']
kangxi = dd['kangxi']
unihan = dd['unihan']
fk = dd['fk']
dfb = dd['dfb']
ccc = dd['ccc']
nvd = dd['nvd']
cxy = dd['cxy']
ylb = dd['ylb']
fxcd = dd['fxcd']
szfs = dd['szfs']
fymyj = dd['fymyj']
wdhy = dd['wdhy']
ldms = dd['ldms']
yzzj = dd['yzzj']
bkqs = dd['bkqs']

# aio = dd['aio']

def lookup(word, dictionary=None, lang='hant', mohu=False):
    '''查字典, dictionary=None表示所有词典, lang表示被查询的语言'''
    pt = re.compile(r'\[|\]|\d')  # 应该在前端过滤
    word = pt.sub('', word)
    print('发过来一个字:%s' % word)

    if TSDinst.detect(word)['confidence'] == 's':
        word = convert2t(word)

    pinyin = ''
    _from = ''
    definition = ''
    if word in fk:
        _from = "佛光山"
        definition = fk[word]
    elif word in dfb:
        _from = dfb[word][0]['usg']
        definition = dfb[word][0]['def']
    elif word in fxcd:
        _from = "于沛煌"
    elif word in ccc:
        _from = "庄春江"
        definition = ccc[word]
    elif word in nvd:
        _from = "南山律"
        definition = nvd[word]
    elif word in cxy:
        _from = "陈孝义"
        definition = cxy[word]
    elif word in ylb:
        _from = "于凌波"
        definition = ylb[word]
    elif word in szfs:
        _from = "三藏法数"
        definition = szfs[word]
    elif word in fymyj:
        _from = "翻譯名義集"
        definition = fymyj[word]
    elif word in wdhy:
        _from = "五燈會元"
        definition = wdhy[word]
    elif word in ldms:
        _from = "歷代名僧辭典"
        definition = ldms[word]
    elif word in yzzj:
        _from = "閱藏知津"
        definition = yzzj[word]
    elif word in bkqs:
        _from = "百科全书"
        definition = bkqs[word]

    if not _from and mohu:
        pass

    return {'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}


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



# 简体繁体转换
def re_search(pattern, string):
    '''对re模块search的改进；把输入字符串使用pattern分割, 每个字符串附带一个标志，表示该字符串是否短语匹配'''
    rr = pattern.search(string)
    if not rr:
        yield (string, False)
        raise StopIteration()
    start, end = rr.span()
    if start !=0:
        yield (string[0:start], False)
    yield (string[start:end], True)
    while True:
        string = string[end:]
        rr = pattern.search(string)
        if not rr: break
        start, end = rr.span()
        if start !=0:
            yield (string[0:start], False)
        yield (string[start:end], True)

    if string:
        yield (string, False)

def __init_cc__():
    '''读取简体繁体转换数据库'''
    # 读取繁体转简体短语字典
    tsptable = dict()
    with open('cc/TSPhrases.txt') as fd:
        for line in fd:
            if line.startswith('#'): continue
            line = line.strip().split()
            tsptable[line[0]] = line[1:][0]

    # 读取简体转繁体转简体短语字典
    stptable = dict()
    with open('cc/STPhrases.txt') as fd:
        for line in fd:
            if line.startswith('#'): continue
            line = line.strip().split()
            stptable[line[0]] = line[1:][0]
    # print('|'.join(sorted(tsptable.keys(), key=lambda x: len(x), reverse=True)))

    # 简体繁体转换pattern
    tsp = re.compile('|'.join(tsptable.keys()))
    stp = re.compile('|'.join(stptable.keys()))

    tstable = dict()
    with open('cc/TSCharacters.txt') as fd:
        for line in fd:
            if line.startswith('#'): continue
            line = line.strip().split()
            tstable[ord(line[0])] = ord(line[1:][0])

    sttable = dict()
    with open('cc/STCharacters.txt') as fd:
        for line in fd:
            if line.startswith('#'): continue
            line = line.strip().split()
            sttable[ord(line[0])] = ord(line[1:][0])
    return tsp, tstable, tsptable, stp, sttable, stptable

    # self.tsp = tsp
    # self.tstable = tstable
    # self.tsptable = tsptable
    # self.stp = stp
    # self.sttable = sttable
    # self.stptable = stptable

tsp, tstable, tsptable, stp, sttable, stptable = __init_cc__()

def convert2s(string, punctuation=True, region=False, autonorm=True, onlyURO=True):
    '''繁体转简体, punctuation是否转换单双引号
    region 是否执行区域转换
    region 转换后的地区
    autonorm 自动规范化异体字
    onlyURO 不简化低位类推简化字(繁体字处于BMP和扩展A区, 但是简体字处于扩展B,C,D,E,F的汉字)
    '''
    if autonorm:
        string = normyitizi(string)

    if punctuation:
        string = string.translate({0x300c: 0x201c, 0x300d: 0x201d, 0x300e: 0x2018, 0x300f: 0x2019})

    # 类推简化字处理
    tstable2 = copy.deepcopy(tstable)
    if onlyURO:
        tstable2 = {k:tstable[k] for k in tstable if not (k < 0x20000 and tstable[k] > 0x20000)}

    content = ''.join(i[0].translate(tstable2) if not i[1] else tsptable[i[0]] for i in re_search(tsp, string))

    return content

def convert2t(string, punctuation=True, region=False):
    '''简体转繁体, punctuation是否转换单双引号
    region 是否执行区域转换
    region 转换后的地区
    '''

    if punctuation:
        string = string.translate({0x201c: 0x300c, 0x201d: 0x300d, 0x2018: 0x300e, 0x2019: 0x300f})

    content = ''.join(i[0].translate(sttable) if not i[1] else stptable[i[0]] for i in re_search(stp, string))

    return content

# 简体繁体转换结束

# 异体字处理

# 读入异体字对照表
yitizi = dict()
with open('dict/variants.txt') as fd:
    for line in fd:
        if line.startswith('#'): continue
        line = line.strip().split()
        yitizi[ord(line[1])] = ord(line[0])

def normyitizi(string, level=0):
    '''异体字规范化为标准繁体字'''
    string = string.translate(yitizi)
    return string

def zi_order(ss, ct):
    '''判断ss字符串中的字是否按照顺序在ct字符串中出现'''
    rr = dict()
    for i, zi in enumerate(ct):
        if zi in rr:
            rr[zi].add(i)
        else:
            rr[zi] = {i}

    result = []
    for zi in ss:
        if zi not in rr:
            return False
        else:
            result.append(rr[zi])

    start = -1
    for i in result:
        start = {j for j in i if j > start}
        if not start:
            return False
        else:
            start = min(start)
    return True

def highlight(ss, ct):
    for zi in set(ss):
        ct = ct.replace(zi, f'<em>{zi}</em>')
    return ct


def fullsearch(ct):
    '''全文搜索'''
    url = "http://127.0.0.1:9200/cbeta/fulltext/_search?"#创建一个文档，如果该文件已经存在，则返回失败
    queryParams = "pretty&size=50"
    url = url + queryParams
    data = {
     "query": {
        "match": {
            "content": {
                "query": ct,
            }
        }
    },
    "highlight": {
        "fields": {
            "content": {

            }
        }
    }
}
    data = {
  "query": {
    "match": {
      "content": ct
    }
  },
  "rescore" : {
    "window_size" : 50,
    "query" : {
      "rescore_query" : {
        "match_phrase" : {
          "content" : {
            "query" : ct,
            "slop" : 50
          }
        }
      }
    }
  }
}

    # 修改其中的keyword
    # tempjason = json.loads(QUERY_TEMPLATE)
    # tempjason["query"]["match"]["content"]["query"] = "天空的雾来的漫不经心"
    # data = json.dumps(tempjason)

    r = requests.get(url, json=data, timeout=10)
    hits = r.json()['hits']['hits']
    result = []
    for i  in hits:
        _source = i["_source"]
        author = _source['author'].split('\u3000')[0]
        juan = _source["filename"].split('n')[0]
        # result.append((''.join(i['highlight']['content']), f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}', _source['title'], author))
        if zi_order(ct, _source['content']):
            result.append({'hl': highlight(ct, _source['content']), 'an': f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}', 'title':_source['title'], 'author': author})
        # else:
        #     import pprint
        #     pprint.pprint(('||'.join(_source['content']), f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}', _source['title'], author))

    return result

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
    print(normyitizi('妬'))

if __name__ == "__main__":
    # main()
    test()


