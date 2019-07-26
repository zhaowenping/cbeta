#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-07-26 10:04:29
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

# tsp, tstable, tsptable, stp, sttable, stptable = __init_cc__()


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
    # string = string.translate(yitizi)
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



with gzip.open('dict/cipin.json.gz') as fd:
    cipind = json.load(fd)

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

    ctx = '骨琑五<g ref="#CB22072">說</g>九種命終心三界<g ref="#CB29911">々</g><g ref="#CB29911">々</g>生各潤生心各有三故<note place="inline">已上'
    ctx = '涌沸彌滿灰水大鐵鑊中，其湯涌沸，上下漂轉。若時銷爛皮肉血脈，唯餘骨琑，爾時漉出'
    # print(rm_ditto_mark(ctx))
    xx = normyitizi(ctx)
    print(ctx)
    print(xx)
    #str_in = "a-kAra"
    #print(hk2iast(str_in))
    #print(hk2iastdeve(str_in))
    # print(convert2t('大佛顶'))
    # ss = Search()
    # for idx in ss.search('大佛頂'):
    #     print(idx)


