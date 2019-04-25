#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-04-25 20:56:09
from __future__ import unicode_literals, division, absolute_import, print_function

"""
函数库
1. 简体繁体检测
2. 简体繁体转换
3. 注音 phonetic notation
4. 注音格式转换
5. 去除'〡'
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
import array
from functools import reduce
import requests


print('调用函数库')


def rm_ditto_mark(ctx):
    # 在xml中去除三个叠字符号: ⺀ U+2E80 0 /〃 U+3003 2227 /々 U+3005 6415/ 亽 U+4EBD 151
    ctx = array.array('u', ctx)
    dittos = (chr(0x3003), chr(0x3005), chr(0x4ebd))
    for idx, zi in enumerate(ctx):
        if zi in dittos:
            for i in range(idx-1, -1, -1):
                if ishanzi(ctx[i]):
                    ctx[idx] = ctx[i]  # 找到一个合法的重复字符进行替换
                    break
    return ctx.tounicode()


def rm_ditto_mark(ctx):
    # 在xml中去除三个叠字符号(默认叠字符号始终相连): ⺀ U+2E80 0 /〃 U+3003 2227 /々 U+3005 6415/ 亽 U+4EBD 151
    ctx = array.array('u', ctx)
    dittos = (chr(0x3003), chr(0x3005), chr(0x4ebd))
    cc = 0  # 叠字符号的重复次数
    len_ctx = len(ctx)
    for idx, zi in enumerate(ctx):
        if zi in dittos:
            cc = cc + 1
            if len_ctx > idx and ctx[idx+1] in dittos:
                continue
        if cc == 0:
            continue
        j = 0
        for i in range(idx-cc, -1, -1):
            if ishanzi(ctx[i]):
                ctx[idx-j] = ctx[i]  # 找到一个合法的重复字符进行替换
                j = j + 1
                cc = cc - 1
                if cc == 0:
                    break
    return ctx.tounicode()


def ishanzi(zi):
    '''判断一个字是否是非叠字汉字'''
    zi = ord(zi)
    # 〇
    if 0x3007 == zi:
        return True
    # 主区
    if 0x4E00 <= zi <= 0x9FEF and zi != 0x4EBD:
        return True
    # A区
    if 0x3400 <= zi <= 0x4DB5:
        return True
    # BCDEF: 0x20007-0x2EBD6
    if 0x20000 <= zi <= 0x2EBE0:
        return True
    # 一些兼容汉字
    if zi in (0x3007, 0xFA1F, 0x2F804, 0x2F83B):
        return True
    return False


def readdb(path, trans=False, reverse=False):
    '''读取文本数据库, trans为是否用于tanslate函数, reverse为是否翻转'''
    result = dict()
    with open(path, encoding='utf8') as fd:
        for line in fd:
            line = line.strip()
            if line.startswith('#') or not line: continue
            c0, c1, *cc = line.strip().split()
            if trans and reverse:
                result[ord(c1)] = ord(c0)
            if trans and not reverse:
                result[ord(c0)] = ord(c1)
            if not trans and reverse:
                result[c1] = c0
            if not trans and not reverse:
                result[c0] = c1
    return result


class TSDetect:
    '''简体繁体检测'''
    def __init__(self):

        self.p = re.compile(r'[\u4e00-\u9fa5]')

        # self.tt: 纯繁体字集合
        # self.ss: 纯简体字集合
        tsdb = readdb('cc/TSCharacters.txt')
        tt = set(tsdb.keys())
        ss = set(tsdb.values())
        xx = tt & ss

        self.tt = tt - xx
        self.ss = ss - xx

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
    print('''读取tab分隔的菜单文件，返回树状字典''')

    with open(sutra_list, encoding='utf8') as fd:
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

def ls(pattern):
    result = []
    for path in os.listdir(pattern):
        if path.startswith(sutra) and re.match(pattern, path):
            result.append(path.split('_')[1][:-4])
    return result

from functools import total_ordering

@total_ordering
class Number:
    '''经号类: T01n0002'''
    def __init__(self, n):
        self.book, self.sutra = n.split('n')
    def __eq__(self, other):
        self.book, self.sutra = n.split('n')
    def __lt__(self, other):
        self.book, self.sutra = n.split('n')


def get_all_juan(number):
    '''给定经号T01n0002，返回所有排序后的卷['001', '002', ...]'''
    book, sutra = number.split('n')
    # 查找第一卷(有些不是从第一卷开始的)
    juan = []
    if not os.path.exists(f'xml/{book}'):
        return None
    for path in os.listdir(f'xml/{book}'):
        if path.startswith(number):
            juan.append(path.split('_')[1][:-4])
    juan.sort(key=lambda x: int(re.sub(r'[a-zA-Z]*', '', f'{x:0<5}'), 16))
    return juan


def get_sorted_juan(book):
    '''获得book(T01)下的所有排序好的经卷号(T01n0002_001)'''
    # 对所有的book下的卷排序
    juanlist = []
    for path in os.listdir(f'xml/{book}'):
        sutra, juan = path[:-4].split('_')
        sutra = sutra.split('n')[1]
        juanlist.append((sutra, juan))
    juanlist.sort(key=lambda x: (int(f'{x[0]:0<5}', 16), int(x[1])))
    juanlist = [f'{book}n{i[0]}_{i[1]:0>3}' for i in juanlist]
    return juanlist


def get_next_juan(number):
    '''给定经号T01n0002_001，返回T01n0002_002'''
    book = number.split('n')[0]
    # 重新生成标准经号
    jinghao, juan = number.split('_')
    number = f'{jinghao}_{juan:0>3}'
    # # 对所有的book下的卷排序
    juanlist = get_sorted_juan(book)

    if number != juanlist[-1]:
        return juanlist[juanlist.index(number) + 1]
    # else: book + 1
    booklist = []
    bookhead = re.sub('[0-9]*', '', book)
    for path in os.listdir(f'xml'):
        if path.startswith(bookhead):
            booklist.append(path.strip(bookhead))
    booklist.sort(key=int)
    booklist = [f'{bookhead}{i}' for i in booklist]
    if book != booklist[-1]:
        nextbook = booklist[booklist.index(book) + 1]
        booklist = get_sorted_juan(nextbook)
        return booklist[0]
    # else:
    return juanlist


def get_prev_juan(number):
    '''给定经号T01n0002_002，返回T01n0002_001'''
    book = number.split('n')[0]
    # 重新生成标准经号
    jinghao, juan = number.split('_')
    number = f'{jinghao}_{juan:0>3}'
    # 对所有的book下的卷排序
    juanlist = get_sorted_juan(book)

    if number != juanlist[0]:
        return juanlist[juanlist.index(number) - 1]
    # else: book - 1
    booklist = []
    bookhead = re.sub('[0-9]*', '', book)
    for path in os.listdir(f'xml'):
        if path.startswith(bookhead):
            booklist.append(path.strip(bookhead))
    booklist.sort(key=int)
    booklist = [f'{bookhead}{i}' for i in booklist]
    if book != booklist[0]:
        prevbook = booklist[booklist.index(book) - 1]
        booklist = get_sorted_juan(prevbook)
        return booklist[-1]
    # else:
    return juanlist


# FROM: https://en.wikipedia.org/wiki/International_Alphabet_of_Sanskrit_Transliteration

# FROM: https://en.wikipedia.org/wiki/Harvard-Kyoto
class SA:
    '''梵语字符串类, 可以使用HK转写和iast转写输入, 使用天城体, 悉檀体, 拉丁输出'''
    pass

def hk2iastdeve(str_in):
    '''hk哈佛-京都系统转IAST梵语(天城体)'''
    sonorants  = {
            # Sonorants:
            'RR': 'ॠ',
            'lR': 'ऌ',
            'lRR': 'ॡ ',
        }

    t1 = {
            # Anusvāra and visarg:
            'aM': 'अं',
            'aH': 'अः',
        # Consonants:
            'ai': 'ऐ',
            'au': 'औ',
            'kh': 'ख',
            'gh': 'घ',
            'ch': 'छ',
            'jh': 'झ',
            'ph': 'फ',
            'Th': 'ठ',
            'Dh': 'ढ',
            'th': 'थ',
            'dh': 'ध',
            'bh': 'भ',
            }

    t2 = {
            'R': 'ऋ',
            # Vowels:
            'a': 'अ',
            'A': 'आ',    # ā
            'i': 'इ',
            'I':'ई',
            'u': 'उ',
            'U':'ऊ',
            'e': 'ए',
            'o': 'ओ',

        # Consonants:
            'k': 'क',
            'g': 'ग',
            'G': 'ङ',
            'c': 'च',
            'j': 'ज',
            'J': 'ञ',
            'T': 'ट',
            'D': 'ड',
            'N': 'ण',
            't': 'त',
            'd': 'द',
            'n': 'न',
            'p': 'प',
            'b': 'ब',
            'm': 'म',
            'y': 'य',
            'r': 'र',
            'l': 'ल',
            'v': 'व',
            'z': 'श',
            'S': 'ष',
            's': 'स',
            'h': 'ह',
            }

        # '@':' ',

    # usedt = {ord(k): ord(t1[k]) for k in t1}
    str_out = str_in.replace('RR', sonorants['RR']).replace('lR', sonorants['lR']).replace('lRR', sonorants['lRR'])
    for zi in t1:
        str_out = str_out.replace(zi, t1[zi])
    for zi in t2:
        str_out = str_out.replace(zi, t2[zi])
    # str_out = str_out.translate(usedt)
    return str_out


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

def HKdict2iast(hkdict):
    # 将HK系统梵文词典转为IAST系统梵文词典
    mwpatten = re.compile(r'(%\{.+?})')
    sa_en = dict()
    # for key in data:
    #     k = key.replace('1', '').replace("'", '').replace('4', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('-', '').lower()
    #     sa_en.update({k: data[key]})

    for key in hkdict:
        vals = hkdict[key]
        devkey = hk2iastdeve(key)
        key = hk2iast(key)  # .replace('1', '').replace("'", '').replace('4', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('-', '') #.lower()
        # 将天城体附加在罗马体后面
        key = ' '.join((key, devkey))
        res = []
        for val in vals:
            x = mwpatten.findall(val)
            if x:
                for ff in x:
                    val = val.replace(ff, hk2iast(ff))
            res.append(val)
        # 不知道以下这两行那个对
        sa_en.update({key: res})
    return sa_en


def load_dict(dictionary=None):

    # 词典列表
    dicts = {'fk': ('佛光山', 'fk.json.gz'), 'dfb': ('丁福保', 'dfb.json.gz'), 'ccc': ('庄春江', 'ccc.json'), 'fxcd': ('法相詞典', 'fxcd.json.gz'),
            'nvd': ('南山律学词典', 'nvd.json.gz'), 'cyx': ('佛學常見詞彙（陳義孝）', 'cyx.json'), 'ylb': ('唯识名词白话新解', 'ylb.json'),
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
                try:
                    v = json.load(fd)
                except:
                    print(path)
                    raise
        else:
            with open(path, encoding='utf8') as fd:
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
    '''查询康熙字典'''

    def sub(word):
        definition = []
        _from = ""
        pinyin = ""
        if word in kangxi:
            _from = "康熙字典"
            kxword = kangxi[word]
            if "說文解字" in kxword:
                definition.append(kxword["說文解字"])
            if "康熙字典" in kxword:
                definition.append(kxword["康熙字典"])
            if "宋本廣韻" in kxword:
                definition.append(kxword["宋本廣韻"])
            if definition:
                definition = '<br><br>'.join(definition)
            else:
                definition = kxword.get('英文翻譯', '')
            pinyin = kxword.get('國語發音', '')
        else:
            _from = "unicode"
            definition = unihan.get(word, {}).get('kDefinition', '')
            pinyin = unihan.get(word, {}).get('kMandarin', '')
        return pinyin, definition, _from

    pinyin, definition, _from = sub(word)

    if not pinyin:
        word2 = normyitizi(word)
        pinyin, definition, _from = sub(word2)
        if definition:
            definition = f'同{word2}<br>' + definition
    return {'word': word, 'pinyin': pinyin, 'def': definition, 'from': _from}


def lookinsa(word):
    definition = sa_hant.get(hk2sa(word).lower(), '')
    pinyin = ""
    _from = ""
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
    return {'word': word, 'pinyin': pinyin, 'def': definition, 'from': _from}


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
cyx = dd['cyx']
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
        definition = '丁福保[{}]'.format(dfb[word][0]['def'])
    elif word in fxcd:
        _from = "朱芾煌"
    elif word in ccc:
        _from = "莊春江"
        definition = ccc[word]
    elif word in nvd:
        _from = "南山律"
        definition = nvd[word]
    elif word in cyx:
        _from = "陈义孝"
        definition = cyx[word]
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

    pinyin = ' '.join(lookinkangxi(zi)['pinyin'] for zi in word)

    if not _from and mohu:
        pass

    return {'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}


class Search:
    def __init__(self, norm=True):
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
        import pprint
        result = [i.split(maxsplit=2) for i in result]
        if norm:
            titles = [(i[0], ' '.join((normyitizi(i[1]), i[2]))) for i in result]
        else:
            titles = [(i[0], ' '.join((i[1], i[2]))) for i in result]
        # pprint.pprint(titles)
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

    def search(self, title, norm=True):
        # title = opencc.convert(title, config='s2t.json')
        # ( for zi in index)
        if norm:
            title = normyitizi(title)
        result = (set(self.index.get(tt, {}).keys()) for tt in list(title))
        return sorted(reduce(lambda x, y: x & y, result), key=pagerank)



# 简体繁体转换
def re_search(pattern, string):
    '''对re模块search的改进；把输入字符串使用pattern分割, 每个字符串附带一个标志，表示该字符串是否短语匹配'''
    rr = pattern.search(string)
    if not rr:
        yield (string, False)
        return
        # raise StopIteration()
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
    # 读取繁体转简体短语词典
    tsptable = readdb('cc/TSPhrases.txt')
    # 读取简体转繁体短语词典
    stptable = readdb('cc/STPhrases.txt')
    # # print('|'.join(sorted(tsptable.keys(), key=lambda x: len(x), reverse=True)))
    # 读取繁体转简体字典
    tstable = readdb('cc/TSCharacters.txt', trans=True)
    # 读取简体转繁体字典
    sttable = readdb('cc/STCharacters.txt', trans=True)

    # 简体繁体转换pattern
    tsp = re.compile('|'.join(tsptable.keys()))
    stp = re.compile('|'.join(stptable.keys()))

    return tsp, tstable, tsptable, stp, sttable, stptable

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
    tst2 = copy.deepcopy(tstable)
    if onlyURO:
        # 只要简化字不在BMP，就是类推简化字
        # tst2 = {k:tstable[k] for k in tstable if not (k < 0x20000 and tstable[k] > 0x20000)}
        # tst2 = {k:tstable[k] for k in tstable if 0x4E00 <= tstable[k] < 0x20000}
        tst2 = {k:tstable[k] for k in tstable if 0x4E00 <= tstable[k] < 0x9FA5}

    content = ''.join(i[0].translate(tst2) if not i[1] else tsptable[i[0]] for i in re_search(tsp, string))

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
yitizi = readdb('dict/variants.txt', True, True)
# 读取异体字短语词典
varptable = readdb('variants/p.txt')
# 异体字转换pattern
varppp = re.compile('|'.join(varptable.keys()))

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

# pun = string.punctuation + '\u00b7\u2013-\u2027\u2e3a\u3000-\u301f\ufe30-\ufe6b\uff01-\uff0f\uff1a-\uff5e'
# pun = re.compile('['+string.punctuation+']')
# 读取标点数据库
pun = dict()
with open('dict/punctuation.txt') as fd:
    for line in fd:
        line = line.strip()
        if not line: continue
        c1 = line[0]
        pun[ord(c1)] = ord(' ')

def hanziin(sentence='', content=''):
    '''判断一段话中是否包含一句话'''
    # 1. 去除标点符号
    sentence = sentence.translate(pun).replace(' ', '')
    content = content.translate(pun).replace(' ', '')
    return sentence in content

def pagerank(filename, sentence='', content=''):
    '''对xml文件名评分, filename 为 T20n1060 或者 T20n1060_001.xml 形式
    A,B,C,D,F,G,GA,GB,I,J,K,L,M,N,P,S,T,U,X,ZW
    '''
    # sentence = sentence.strip().split()
    # sentence_value = sum([{True:0, False:1}[s in content] for s in sentence])
    pr = ("T", "B", "ZW", "A", "C", "D", "F", "G" , "GA", "GB", "I", "J", "K", "L", "M", "N", "P", "S", "U", "X")
    pt = re.compile(r'\d+')  # 应该在前端过滤
    if filename[0] == 'T':
        r = 0
    else:
        r = 1
    x = pt.findall(filename)
    x = [int(i) for i in x]
    # return r, x[0], x[1], x[2]
    x.insert(0, r)
    # x.insert(0, sentence_value)
    return x


def fullsearch(sentence):
    '''全文搜索'''
    # sentence2 = sentence.replace(' ', '')
    url = "http://127.0.0.1:9200/cbeta/fulltext/_search?"#创建一个文档，如果该文件已经存在，则返回失败
    queryParams = "pretty&size=50"
    url = url + queryParams
    data = {
     "query": {
        "match": {
            "content": {
                "query": sentence,
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
      "content": sentence
    }
  },
  "rescore" : {
    "window_size" : 50,
    "query" : {
      "rescore_query" : {
        "match_phrase" : {
          "content" : {
            "query" : sentence,
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
        if zi_order(sentence, _source['content']):
            result.append({'hl': highlight(sentence, _source['content']), 'an': f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}',
                'title':_source['title'], 'author': author, 'content': _source['content'],
                'filename': _source["filename"].split('.')[0]})

    # sorted(result, key=lambda x: pagerank(x['filename']), reverse=True)
    result.sort(key=lambda x: pagerank(x['filename']))  #, sentence, x['content']))
        # else:
        #     import pprint
        #     pprint.pprint(('||'.join(_source['content']), f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}', _source['title'], author))

    return result

with gzip.open('dict/cipin.json.gz') as fd:
    cipind = json.load(fd)

def zhuyin(txt, ruby=False, cipin=50):
    '''對txt文本注音, ruby是否使用ruby語法'''
    if not ruby:
        content = ' '.join(lookinkangxi(i)['pinyin'].split(' ')[0] for i in txt)
    else:
        result = []
        for zi in txt:
            if cipind.get(zi, 0) < cipin:
                pinyin = lookinkangxi(zi)['pinyin'].split(' ')[0]
                if pinyin:
                    zi = f"<ruby>{zi}<rt>{pinyin}</rt></ruby>"
            result.append(zi)
        content = ''.join(result)
    return content

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


import difflib
from difflib import *

def diff_ctx(lctx, rctx):
    '''比较两个文本的不同, 使用html排版'''

    d = Differ()
    result = d.compare(lctx, rctx)

    lctx = []
    rctx = []
    for line in result:
        if line.startswith(' '):
            line = line[2:]
            lctx.append(line)
            rctx.append(line)
        elif line.startswith('- '):
            line = line[2:]
            lctx.append(f'<span class="red">{line}</span>')
        elif line.startswith('+ '):
            line = line[2:]
            rctx.append(f'<span class="red">{line}</span>')
        elif line.startswith('?'):
            continue
    lctx = ''.join(lctx)
    rctx = ''.join(rctx)
    lctx = ''.join(f'<p>{line}</p>' for line in lctx.splitlines())
    rctx = ''.join(f'<p>{line}</p>' for line in rctx.splitlines())

    return {'lfile': lctx, 'rfile': rctx}


def test():
    ''''''
    print(normyitizi('妬'))

if __name__ == "__main__":
    # main()
    # test()
    # print(get_all_juan('T02n0099'))
    # print(get_all_juan('GA031n0032'))
    # print(get_all_juan('J31nB269'))
    # print(get_all_juan('T19n0974A'))
    # print(get_next_page('T02n0099_001'))
    # print(get_next_page('T01n0002_001'))

    # with gzip.open('dict/kangxi.json.gz') as fd:
    #     kangxi = json.load(fd)

    # with open('cipin.json') as fd:
    #     cipin = json.load(fd)

    # for word in kangxi:
    #     kxword = kangxi[word]
    #     pinyin = kxword.get('國語發音', '')
    #     if not pinyin:
    #         word2 = normyitizi(word)
    #         kxword2 = kangxi.get(word2, {})
    #         pinyin2 = kxword2.get('國語發音', '')
    #         if pinyin2:
    #             # print(word, word2, pinyin2)
    #             pass
    #         else:
    #             cp = cipin.get(word, 0)
    #             if cp > 0:
    #                 print(word, word2, cipin.get(word, 0), "%X" % ord(word))
    #             pass
    # print(pagerank('T14n0563_001.xml'))
    # print(zhuyin('你好', True))
    print(lookinkangxi('𢾛'))

    #str_in = "a-kAra"
    #print(hk2iast(str_in))
    #print(hk2iastdeve(str_in))
    print(convert2t('大佛顶'))
    # ss = Search()
    # for idx in ss.search('大佛頂'):
    #     print(idx)


