#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2020-01-31 04:15:07
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
import pprint
import unicodedata

import requests


print('调用函数库')


def rm_html_tag(title):
    # 去除HTML标签、注释、卷数, 留下标题
    title = re.sub(r'<.*?>', '', title)  # title=[34]<span style="color:red">阿</span>差末菩薩經
    title = re.sub(r'\(.*?\)', '', title)
    title = re.sub(r'\[\w*?\]', '', title)
    title = re.sub(r'[一二三四五六七八九十百]+卷', '', title)
    return title

def rm_com(ctx):
    # 删除组字式
    for com in re.findall(r'\[.*?\]', ctx):
        pass
    pass


def rm_joiner(ctx):
    '''去除汉字的链接和装饰符号: 外圈加方框或者圆形'''
    tt = {0x200C:0xFFFD, 0x200D:0xFFFD, 0x20DD:0xFFFD, 0x20DE:0xFFFD, 0x20DF:0xFFFD, 0x20E0:0xFFFD}
    ctx = ctx.translate(tt).replace(chr(0xFFFD), '')
    return ctx


# _space = re.compile(r'[ \t\n\r\x0b\x0c\u3000]+')
def normalize_space(ctx):
    '''去掉字符串两边的空格, 中间连续的多个空格替换为一个'''
    ctx = ctx.strip()
    ctx = re.sub(r'\s+', ' ', ctx)
    return ctx


def rm_ditto_mark(ctx):
    # 在xml中去除三个叠字符号(默认叠字符号始终相连): ⺀ U+2E80 0 /〃 U+3003 2227 /々 U+3005 6415/ 亽 U+4EBD 151
    # 首先删除叠字符号中间的空白
    ctx = re.sub(r'([\u3003\u3005\u4ebd])\s+([\u3003\u3005\u4ebd])', r'\1\2', ctx)
    ctx = array.array('u', ctx)
    dittos = (chr(0x3003), chr(0x3005), chr(0x4ebd))
    cc = 0  # 叠字符号的重复次数
    len_ctx = len(ctx)
    for idx, zi in enumerate(ctx):
        if zi in dittos:
            cc = cc + 1
            if len_ctx > idx+1 and ctx[idx+1] in dittos:
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
    '''判断一个字符是否是非叠字汉字'''
    zi = ord(zi)
    # 〇
    if 0x3007 == zi:
        return True
    # A区
    if 0x3400 <= zi <= 0x4DB5:
        return True
    # 主区
    if 0x4E00 <= zi <= 0x9FEF and zi != 0x4EBD:
        return True
    # BCDEF: 0x20007-0x2EBD6
    if 0x20000 <= zi <= 0x2EBE0:
        return True
    # 兼容汉字区
    if 0xF900 <= zi <= 0xFAD9:
        return True
    if 0x2F800 <= zi <= 0x2FA1D:
        return True
    return False


def readdb(path, trans=False, reverse=False):
    '''读取文本数据库, trans为是否用于tanslate函数, reverse为是否翻转'''
    result = dict()
    # path = os.path.join("/home/zhaowp/cbeta/cbeta", path)
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


def normalize_text(ctx):
    '''标准化文本'''
    # 去除两边空格及多余空格
    ctx = normalize_space(ctx)
    # 去除汉字链接符号
    ctx = rm_joiner(ctx)
    # 去除汉字重复符号
    ctx = rm_ditto_mark(ctx)
    # 去除异体字、异体词
    ctx = rm_variant(ctx)
    # 去除标点符号?
    return ctx


from functools import total_ordering

@total_ordering
class Number:
    '''经号类: T01n0002a'''
    def __init__(self, n):
        self.book, self.sutra = n.split('n')
    def __eq__(self, other):
        self.book, self.sutra = n.split('n')
    def __lt__(self, other):
        self.book, self.sutra = n.split('n')
    def __str__(self):
        pass

class Sutra:
    def __init__(self, args):
        self.title = args[0]  # 经名
        self.number = args[1] # 经号
        self.author = args[2] # 作者
        self.total = args[3] # 卷数/字数, 年代


def get_all_juan(number):
    '''给定经号T01n0002，返回所有排序后的卷['001', '002', ...]
    返回值是一个数组，如果没有找到则返回空的数组'''
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

def get_sorted_ce(book):
    # 获得全部book(T01)下的所有排序好的册号列表(T01,T02,T03,T04...)
    booklist = []
    bookhead = re.sub('[0-9]*', '', book)
    for path in os.listdir(f'xml'):
        if path.startswith(bookhead):
            booklist.append(path.strip(bookhead))
    booklist.sort(key=int)
    booklist = [f'{bookhead}{i}' for i in booklist]
    return booklist

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
    # 获得全部排序号的book列表
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


sch_db = []
with open("static/sutra_sch.lst") as fd:
    for line in fd:
        if 'n' in line:
            line = line.strip().split()[0]
            sch_db.append(line)

# 大正七〇·四五九中、四六〇下
# 大正藏第70卷459页b
def make_url2():
    # 大正四五·九下
    # 0009c01
    # vol:45;page:p9c
    # vol:30;page:p772c
    t = { '〇': '0',
          '一': '1',
          '二': '2',
          '三': '3',
          '四': '4',
          '五': '5',
          '六': '6',
          '七': '7',
          '八': '8',
          '九': '9',
          '上': 'a',
          '中': 'b',
          '下': 'c',
            }
    pass

# 模式1: T01n0001, T01n0001_001, T01n0001_p0001a01
# 模式2: T01,no.1,p.1a1
# CBETA 2019.Q2, Y25, no. 25, p. 411a5-7
# CBETA, T14, no. 475, pp. 537c8-538a14
# 模式0: 100, '100,3', t1000, t1000_001
# TODO: T20n1113B
# TODO: 大宝积经100
# jinghaopatten = re.compile(r'([a-zA-Z]{1,2})(\d{2,3})n(\d{4})([a-zA-Z])?(?:_(\d{3}))?(?:[_#](p\d{4}[abc]\d\d))?')
jinghaopatten = re.compile(r'([a-zA-Z]{1,2})(\d{2,3})n(\d{4})(?:_(\d{3}))?(?:[_#](p\d{4}[abc]\d\d))?')
jinghaopatten2 = re.compile(r'([a-zA-Z]{1,2})(\d{2,3}),\s*no\.\s*(\d+),\s*pp?\.\s*(\d+)([abc])(\d+)')
jinghaopatten0 = re.compile(r'([a-zA-Z]{1,2})?(\d+)[ \t,._\u3000\u3002\uff0c-]+(\d+)')  # 全角逗号句号
# jinghaopatten0 = re.compile(r'([\u3007\u3400-\u9FCB\U00020000-\U0002EBE0]+)[ \t,._\u3000\u3002\uff0c-]*(\d+)')
def make_url(title):
    j1, j2, j3, j4, j5 = 'T', '', '', '', ''
    # j1, j2,   j3,  j4, j5
    #  T, 01, 0001, 001, p0001a01
    # j6如果是小写就变为大写, 大写就变成小写
    # j6 = j6.upper() if ord('a') <= ord(j6) <= ord('z') else j6.lower()
    found = False
    if not found:
        jinghao = jinghaopatten.findall(title)
        if jinghao:
            j1,j2,j3,j4,j5 = jinghao[0]
            found = True

    if not found:
        jinghao = jinghaopatten2.findall(title)
        if jinghao:
            j1,j2,j3,j5,j6,j7 = jinghao[0]
            j5 = 'p{:04}{}{:02}'.format(int(j5), j6, int(j7))
            found = True

    if not found:
        jinghao = jinghaopatten0.findall(title)
        if jinghao:
            j1,j3,j4 = jinghao[0]
            found = True

    if title.isdigit():
        j3 = '{:04}'.format(int(title))
        found = True

    if not found:
            return None

    j1 = j1.upper() if j1 else 'T'
    j3 = '{:04}'.format(int(j3))
    # 查找册数 # TODO: 根据锚来查找册数
    if not j2:
        for line in sch_db:
            if j1 in line and j3 in line:
                j2 = line.split('n')[0][len(j1):]
                break
    if not j2:
        return None

    # 查找卷数
    if not j4:
        j4 = get_all_juan(f'{j1}{j2}n{j3}')
        if j4:
            j4 = j4[0]

    if not j4:
        return None

    j4 = '{:03}'.format(int(j4))
    # 如果有锚就添加锚
    if j5:
        url = f'xml/{j1}{j2}/{j1}{j2}n{j3}_{j4}.xml#{j5}'
    else:
        url = f'xml/{j1}{j2}/{j1}{j2}n{j3}_{j4}.xml'
    return url


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
        word2 = rm_variant(word)
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
            titles = [(i[0], ' '.join((rm_variant(i[1]), i[2]))) for i in result]
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
            title = rm_variant(title)
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


class STConvertor:
    '''简体繁体转换类'''
    def __init__(self):
        '''读取简体繁体转换数据库'''
        # 读取繁体转简体短语词典
        self.tsptable = readdb('cc/TSPhrases.txt')
        # 读取简体转繁体短语词典
        self.stptable = readdb('cc/STPhrases.txt')
        # # print('|'.join(sorted(tsptable.keys(), key=lambda x: len(x), reverse=True)))
        # 读取繁体转简体字典
        self.tstable = readdb('cc/TSCharacters.txt', trans=True)
        # 读取简体转繁体字典
        self.sttable = readdb('cc/STCharacters.txt', trans=True)

        # 简体繁体转换pattern
        self.tsp = re.compile('|'.join(self.tsptable.keys()))
        self.stp = re.compile('|'.join(self.stptable.keys()))

        # return tsp, tstable, tsptable, stp, sttable, stptable

        # 简体繁体检测
        self.p = re.compile(r'[\u4e00-\u9fa5]')

        _tst = readdb('cc/TSCharacters.txt')
        # self.tt: 纯繁体字集合
        # self.ss: 纯简体字集合
        tt = set(_tst.keys())
        ss = set(_tst.values())
        xx = tt & ss

        self.tt = tt - xx
        self.ss = ss - xx


    def t2s(self, string, punctuation=True, region=False, autonorm=True, onlyURO=True):
        '''繁体转简体, punctuation是否转换单双引号
        region 是否执行区域转换
        region 转换后的地区
        autonorm 自动规范化异体字
        onlyURO 不简化低位类推简化字(繁体字处于BMP和扩展A区, 但是简体字处于扩展B,C,D,E,F的汉字)
        '''
        if autonorm:
            string = rm_variant(string)

        if punctuation:
            string = string.translate({0x300c: 0x201c, 0x300d: 0x201d, 0x300e: 0x2018, 0x300f: 0x2019})

        # 类推简化字处理
        tst2 = copy.deepcopy(self.tstable)
        if onlyURO:
            # 只要简化字不在BMP，就是类推简化字
            # tst2 = {k:tstable[k] for k in tstable if not (k < 0x20000 and tstable[k] > 0x20000)}
            # tst2 = {k:tstable[k] for k in tstable if 0x4E00 <= tstable[k] < 0x20000}
            tst2 = {k:self.tstable[k] for k in self.tstable if 0x4E00 <= self.tstable[k] < 0x9FA5}
        else:
            tst2 = {k:self.tstable[k] for k in self.tstable}

        content = ''.join(i[0].translate(tst2) if not i[1] else self.tsptable[i[0]] for i in re_search(self.tsp, string))

        return content


    def s2t(self, string, punctuation=True, region=False):
        '''简体转繁体, punctuation是否转换单双引号
        region 是否执行区域转换
        region 转换后的地区
        '''

        if punctuation:
            string = string.translate({0x201c: 0x300c, 0x201d: 0x300d, 0x2018: 0x300e, 0x2019: 0x300f})

        content = ''.join(i[0].translate(self.sttable) if not i[1] else self.stptable[i[0]] for i in re_search(self.stp, string))

        return content


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

        confidence = 's'
        if t > 50:
            confidence = 't'
        elif s > 50:
            confidence = 's'
        elif t > s:
            confidence = 't'

        return {'t': t, 's': s, 'confidence': confidence}


# 异体字处理

# 读入异体字对照表
yitizi = readdb('dict/variants.txt', True, True)
# 读取异体字短语词典
varptable = readdb('variants/p.txt')
# 异体字转换pattern
varppp = re.compile('|'.join(sorted(varptable.keys(),key=len,reverse=True)))

def rm_variant(string, level=0):
    '''异体字规范化为标准繁体字'''
    # string = string.translate(yitizi)
    # return string
    # ctx = unicodedata.normalize("NFKC", ctx)
    content = ''.join(i[0].translate(yitizi) if not i[1] else varptable[i[0]] for i in re_search(varppp, string))
    return content


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
        if line.startswith('~~~~~~~~~'):
            break
        if not line or line.startswith('#'): continue
        c1 = line[0]
        pun[ord(c1)] = 0xFFFD

def rm_pun(ctx):
    '''删除标点符号'''
    ctx = ctx.translate(pun).replace(chr(0xFFFD), '')
    return ctx


def pagerank(filename, sentence='', content=''):
    '''对xml文件名评分, filename 为 T20n1060 或者 T20n1060_001.xml 形式
    A,B,C,D,F,G,GA,GB,I,J,K,L,M,N,P,S,T,U,X,ZW, Y, LC
    '''
    # sentence = sentence.strip().split()
    # sentence_value = sum([{True:0, False:1}[s in content] for s in sentence])
    pr = ("T", "B", "ZW", "A", "C", "D", "F", "G" , "GA", "GB", "I", "J", "K", "L", "M", "N", "P", "S", "U", "X", "Y", "LC")
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


# XXX convert2t
def search_title(title):
    '''通过标题搜索'''
    if request.method == "GET":
        title = request.GET.title
        # 去除HTML标签、注释、卷数, 留下标题
        title = re.sub(r'<.*?>', '', title)  # title=[34]<span style="color:red">阿</span>差末菩薩經
        title = re.sub(r'\(.*?\)', '', title)
        title = re.sub(r'\[\w*?\]', '', title)
        title = re.sub(r'[一二三四五六七八九十百]+卷', '', title)
    else:
        title = request.forms.content
    if ts.detect(title)['confidence'] == 's':
        # title = opencc.convert(title, config='s2t.json')
        title = convert2t(title)
    results = []
    if not title:
        return {'results': results}
    for idx in ss.search(title):
        title0 = idx
        hl = ss.titles[idx]
        zang = idx.split('n')[0]              # T01
        juan = get_all_juan(idx)[0]           # 001
        an = f"/xml/{zang}/{idx}_{juan}.xml"  # T01n0002_001.xml
        results.append({'hl': hl, 'an':an, 'title':title0, 'author':''})
    if request.method == "GET":
        # 0个结果页面不动, 多个结果自己选择
        if len(results) == 0:
            abort(304)
        if len(results) == 1:
            redirect(an)
        if len(results) > 1:
            pass
    return {'results': results}



def must_search(sentence, _from=0, _end=5000):
    print('must搜索:', sentence)
    url = "http://127.0.0.1:9200/cbeta/_doc/_search" #创建一个文档，如果该文件已经存在，则返回失败
    data = {
     "query": {
        # "match_phrase": { "content": sentence # "content": {"query": sentence, "slop": 1} },
         "bool":{
            #  "must": {}
        }
    },
    "size":_end - _from ,
    "from": _from,
    "highlight": {
        "fields": {
            "raw": {

            }
        }
    }
    }


    # if re.search(r'\s+or\s+|\s*\|\s*', sentence, flags=re.I):
    #     sentences = re.split(r'\s+or\s+|\s*\|\s*', sentence, flags=re.I)
    #     data["query"]["bool"]["should"] = [{"match_phrase": { "content": st}} for st in sentences]
    # else:
    sentences = re.split(r'\s+and\s+|\s*&\s*|\s+', sentence, flags=re.I)
    # data["query"]["bool"]["must"] = [{"match_phrase": {"content": st}} for st in sentences]
    sentences = [re.split(r':|：', st) for st in sentences]
    data["query"]["bool"]["must"] = [{"match_phrase": {"content": st[0]}} if len(st) == 1 else {"match": {st[0].lower(): st[1]}} for st in sentences]
    pprint.pprint(data["query"]["bool"]["must"])

    r = requests.get(url, json=data, timeout=10)
    result = r.json()
    return result


def fullsearch(sentence):
    '''全文搜索, sentence是繁体字'''
    sentence = normalize_text(sentence)
    r = must_search(sentence)
    hits = r['hits']['hits']
    result = []
    for hit in hits:
        _source = hit["_source"]
        author = _source['author']  # .split('\u3000')[0]
        juan = _source["filename"].split('n')[0]
        hl = highlight(sentence, _source["raw"])
        # 文章内容去除标点符号
        result.append({'hl': hl, 'an': f'/xml/{juan}/{_source["filename"]}.xml#{hit["_id"]}',
                'title':_source['title'], 'author': author,
                # 'content': _source['raw'],
                'filename': _source["filename"]})

    result.sort(key=lambda x: pagerank(x['filename']))

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
    # lctx = ''.join(f'<p>{line}</p>' for line in lctx.splitlines())
    # rctx = ''.join(f'<p>{line}</p>' for line in rctx.splitlines())

    return {'lfile': lctx, 'rfile': rctx}


def test():
    ''''''
    print(rm_variant('妬'))

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
    #         word2 = rm_variant(word)
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
    # print(lookinkangxi('𢾛'))

    # ctx = '五<g ref="#CB22072">說</g>九種命終心三界<g ref="#CB29911">々</g><g ref="#CB29911">々</g>生各潤生心各有三故<note place="inline">已上'
    # print(rm_ditto_mark(ctx))
    #str_in = "a-kAra"
    #print(hk2iast(str_in))
    #print(hk2iastdeve(str_in))
    # print(convert2t('大佛顶'))
    # ss = Search()
    # for idx in ss.search('大佛頂'):
    #     print(idx)
    # # TODO:搜索t1000, t1000_001, T01n0001, T01n0001_001, T01n0001_p0001a01, T01,no.1,p.1a1
    #titlepatten = re.compile(r'([a-zA-Z][a-zA-Z]?)(\d\dn)?(\d\d\d\d)(_\d\d\d)?')
    #titlepatten.find('t1000')
    #import pprint
    #with open("static/sutra_sch.lst") as fd:
    #    for line in fd:
    #        if 'n' in line:
    #            line = line.strip().split()
    #            print(line)
    #pprint.pprint(mulu)
    # print(make_url('CBETA, T14, no. 475, pp. 537c8-538a14'))
    # print(make_url('CBETA 2019.Q2, Y25, no. 25, p. 411a5-7'))
    # print(normalize_text('說</g>九種命終心三界'))
    #for i in fullsearch('止觀明靜'):
    #    print(i)
    stc = STConvertor()
    print(stc.t2s('那莫三𭦟多嚩日羅赦憾云〃哦'))
    print(stc.s2t('安乐国'))
    print(stc.detect('安乐国'))
    print(stc.detect('那莫三𭦟多嚩日羅赦憾云〃哦'))


