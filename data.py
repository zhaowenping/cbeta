#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2021-02-12 15:35:40
from __future__ import unicode_literals, division, absolute_import, print_function

"""
统一处理数据库载入,将入口改为从redis读取
"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


import re
import json
import gzip

import redis
import msgpack
import requests

from libhan import rm_variant, python_escape, python_unescape

REDIS_HOST= 'localhost'


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


def main():
    '''装入所有数据'''

    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

    # 删除数据库所有内容
    for k in r.keys('*'):
        r.delete(k)

    # 重建数据库

    # tsptable = readdb('cc/TSPhrases.txt')
    # r.hset('tsptable', mapping=tsptable)
    #
    # stptable = readdb('cc/STPhrases.txt')
    # r.hset('stptable', mapping=stptable)
    #
    # tstable = readdb('cc/TSCharacters.txt', trans=True)
    # r.hset('tstable', mapping=tstable)
    #
    # sttable = readdb('cc/STCharacters.txt', trans=True)
    # r.hset('sttable', mapping=sttable)
    #
    # _tst = readdb('cc/TSCharacters.txt')
    # yitizi = readdb('dict/variants.txt', True, True)
    # varptable = readdb('variants/p.txt')
    #
    # ids_dict = dict()
    # with open('idx/ids.txt') as fd:
    #     for line in fd:
    #         line = line.strip().split()
    #         ids_dict[line[2]] = line[1]
    # r.hset('ids_dict', mapping=ids_dict)
    #
    # with open('idx/composition.json') as fd:
    #     com_dict = json.load(fd)
    # r.hset('com_dict', mapping=com_dict)
    #
    #     with open(path, encoding='utf8') as fd:
    #     with open(sutra_list, encoding='utf8') as fd:
    #     with open(filepath) as fd:
    # #with open(os.path.join(PATH, "idx/sutra_sch.lst")) as fd:
    # with open("idx/sutra_sch.lst") as fd:
    #         with open(f'idx/{book}.xml') as fd:
    #         with open('idx/pbidx.txt') as fd:
    #         with gzip.open(f'idx/lb/{book}{tome}n{sutra}{j4}.gz', 'rt') as fd:
    #     # with gzip.open('dict/sa-en.json.gz') as fd:
    #     # with gzip.open('dict/sa-hant.json.gz') as fd:
    #     # with gzip.open('dict/yat.json.gz') as fd:
    #     with open('dict/Unihan_Readings.json') as fd:
    #             with gzip.open(path) as fd:
    #             with open(path, encoding='utf8') as fd:
    #         with open("idx/sutra_sch.lst") as fd:
    #         # title = opencc.convert(title, config='s2t.json')
    #         with open('idx/jt.txt') as fd:
    # with open('dict/punctuation.txt') as fd:
    # with gzip.open('dict/cipin.json.gz') as fd:
    #     import opencc
    #     title = opencc.convert(title, config='s2t.json')
    #     # with gzip.open('dict/kangxi.json.gz') as fd:
    #     # with open('cipin.json') as fd:
    #     #with open("static/sutra_sch.lst") as fd:
    #

    # 装入康熙字典
    with gzip.open('dict/kangxi.json.gz') as fd:
        kangxi = json.load(fd)

        kangxi = {k: msgpack.dumps(kangxi[k]) for k in kangxi}
        r.hset('dict_kangxi', mapping=kangxi)

    # 装入unihan
    with open('dict/Unihan_Readings.json') as fd:
        unihan = json.load(fd)
        unihan = {k: msgpack.dumps(unihan[k]) for k in unihan}
        r.hset('dict_unihan', mapping=unihan)

    # 佛光大辭典
    with gzip.open('dict/fk.json.gz') as fd:
        fk = json.load(fd)
        fk.pop('header', None)
        r.hset('dict_fk', mapping=fk)

    # 丁福保佛學大詞典
    with gzip.open('dict/dfb.json.gz') as fd:
        dfb = json.load(fd)
        dfb.pop('header', None)
        dfb = {k: '\n'.join(i['def'] for i in dfb[k]) for k in dfb}
        r.hset('dict_dfb', mapping=dfb)

    # 阿含辭典 - 莊春江居士編
    with open('dict/ccc.json') as fd:
        ccc = json.load(fd)
        ccc.pop('header', None)
        r.hset('dict_ccc', mapping=ccc)

    # 法相辭典
    with gzip.open('dict/fxcd.json.gz') as fd:
        fxcd = json.load(fd)
        fxcd.pop('header', None)
        r.hset('dict_fxcd', mapping=fxcd)


    # 南山律學辭典
    with gzip.open('dict/nvd.json.gz') as fd:
        nvd = json.load(fd)
        nvd.pop('header', None)
        r.hset('dict_nvd', mapping=nvd)


    # 陳義孝佛學常見辭匯
    with open('dict/cyx.json') as fd:
        cyx = json.load(fd)
        cyx.pop('header', None)
        r.hset('dict_cyx', mapping=cyx)


    # 于凌波词典 -- 唯識名詞白話新解
    with open('dict/ylb.json') as fd:
        ylb = json.load(fd)
        ylb.pop('header', None)
        r.hset('dict_ylb', mapping=ylb)


    # 三藏法數
    with open('dict/szfs.json') as fd:
        szfs = json.load(fd)
        szfs.pop('header', None)
        szfs = {k: szfs[k]['def'] for k in szfs}
        r.hset('dict_szfs', mapping=szfs)


    # 翻譯名義集
    with open('dict/fymyj.json') as fd:
        fymyj = json.load(fd)
        fymyj.pop('header', None)
        r.hset('dict_fymyj', mapping=fymyj)


    # 五燈會元
    with gzip.open('dict/wdhy.json.gz') as fd:
        wdhy = json.load(fd)
        wdhy.pop('header', None)
        r.hset('dict_wdhy', mapping=wdhy)


    # 閱藏知津
    with gzip.open('dict/yzzj.json.gz') as fd:
        yzzj = json.load(fd)
        yzzj.pop('header', None)
        r.hset('dict_yzzj', mapping=yzzj)


    # 歷代名僧詞典
    with gzip.open('dict/ldms.json.gz') as fd:
        ldms = json.load(fd)
        ldms.pop('header', None)
        r.hset('dict_ldms', mapping=ldms)


    # 俗語佛源
    with gzip.open('dict/syfy.json.gz') as fd:
        syfy = json.load(fd)
        syfy.pop('header', None)
        r.hset('dict_syfy', mapping=syfy)


    # 中華佛教百科全書
    with gzip.open('dict/bkqs.json.gz') as fd:
        bkqs = json.load(fd)
        bkqs.pop('header', None)
        r.hset('dict_bkqs', mapping=bkqs)


    # class DICT:
    #     def __init__(self, key):
    #         r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    #         pass

def test():
    ''''''

def load_dict(dictionary=None):

    # 词典列表
    dicts = {'fk': ('佛光山', 'fk.json.gz'), 'dfb': ('丁福保', 'dfb.json.gz'), 'ccc': ('庄春江', 'ccc.json'), 'fxcd': ('法相詞典', 'fxcd.json.gz'),
            'nvd': ('南山律学词典', 'nvd.json.gz'), 'cyx': ('佛學常見詞彙（陳義孝）', 'cyx.json'), 'ylb': ('唯识名词白话新解', 'ylb.json'),
            'szfs': ('三藏法数', 'szfs.json'), 'fymyj': ('翻譯名義集', 'fymyj.json'), 'wdhy': ('五燈會元', 'wdhy.json.gz'), 'yzzj': ('閱藏知津', 'yzzj.json.gz'),
            'ldms': ('歷代名僧辭典', 'ldms.json.gz'), 'syfy': ('俗語佛源', 'syfy.json.gz'), 'bkqs': ('中华佛教百科全书','bkqs.json.gz')}


# for k in ccc:
#     if not isinstance(ccc[k], str):
#         print(k, ccc[k])

def lookup(word, dictionary=None, lang='hant', mohu=False):
    '''查字典, dictionary=None表示所有词典, lang表示被查询的语言'''

    r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

    # with r.pipeline(transaction=False) as pipe:
    # pipe.execute()

    pinyin = ''
    definition = []

    val = r.hget('dict_fk', word)
    if val:
        definition.append(f"《佛光山》: {val}")

    val = r.hget('dict_dfb', word)
    if val:
        definition.append(f"《丁福保》: {val}")

    val = r.hget('dict_fxcd', word)
    if val:
        definition.append(f"《朱芾煌》: {val}")

    val = r.hget('dict_ccc', word)
    if val:
        definition.append(f"《莊春江》: {val}")


    val = r.hget('dict_szfs', word)
    if not definition and val:
        definition.append(f"《三藏法數》: {val}")

    val = r.hget('dict_fymyj', word)
    if not definition and val:
        definition.append(f"《翻譯名義集》: {val}")

    val = r.hget('dict_wdhy', word)
    if not definition and val:
        definition.append(f"《五燈會元》: {val}")

    val = r.hget('dict_nvd', word)
    if not definition and val:
        definition.append(f"《南山律》: {val}")

    val = r.hget('dict_cyx', word)
    if not definition and val:
        definition.append(f"《陳義孝》: {val}")

    val = r.hget('dict_ylb', word)
    if not definition and val:
        definition.append(f"《于凌波》: {val}")

    val = r.hget('dict_ldms', word)
    if not definition and val:
        definition.append(f"《歷代名僧辭典》: {val}")

    val = r.hget('dict_yzzj', word)
    if not definition and val:
        definition.append(f"《閱藏知津》: {val}")

    val = r.hget('dict_bkqs', word)
    if not definition and val:
        definition.append(f"《百科全书》: {val}")

    definition = '\n\n'.join(definition)
    definition = definition.replace('\n', '<br>')

    # pinyin = ' '.join(lookinkangxi(zi)['pinyin'] for zi in word)
    if definition:
        pinyin = lookinkangxi_pinyin(word)
	# # 用Unicode数据库注音
	# if _from and not pinyin:
	#     pinyin = [unihan.get(x, {}).get('kMandarin', '') for x in word]
	#     pinyin = ' '.join([x.split()[0] if x else '' for x in pinyin])

    r.close()
    return {'word': word, 'pinyin': pinyin, 'definition': definition, 'from': ''}


def lookup(word, dictionary=None, lang='hant', mohu=False):
    # nword = normalize_text(word)
    nword = ''.join(python_escape(word))
    url = "http://127.0.0.1:9200/dict/_doc/_search"
    data = {
     "query": {
         # "match_phrase": { "orth": nword},  # "content": {"query": sentence, "slop": 1} },
         "match_phrase": {"hyph": nword},  # "content": {"query": sentence, "slop": 1} },
       #  "bool":{
            #  "must": {}
       # }
    },
    # "size": 20,
    # "from": 0,
    }
    r= requests.get(url, json=data, timeout=10)
    result = r.json()
    import pprint
    # result['hits'].pop('hits')
    # pprint.pprint(result)
    hits = result['hits']['hits']
    # print(len(hits))
    result = []
    for hit in hits:
        _source = hit["_source"]
        # 文章内容高亮显示
        result.append({'definition': _source['def'], 'word':python_unescape(_source['hyph']), 'from': _source['dict']})

    # result.sort(key=lambda x: pagerank(x['number']))
    # pprint.pprint(result)
    result = [f'{it["from"]}: {it["definition"]}' for it in result]
    definition = '<br>'.join(result)
    pinyin = ''
    return {'word': word, 'pinyin': pinyin, 'definition': definition, 'from': ''}


def lookinkangxi_pinyin(word):
    '''在康熙字典中查找句子的拼音'''

    r2 = redis.Redis(host=REDIS_HOST, port=6379)
    with r2.pipeline(transaction=False) as pipe:
        pipe.hmget('dict_kangxi', *word)
        result = pipe.execute()
    r2.close()

    result = [msgpack.loads(val) if val else dict() for val in result[0]]
    result = ' '.join([val['國語發音'] if '國語發音' in val else '*' for val in result])
    return result


def lookinkangxi(word):
    '''在康熙字典中查一个字'''

    r2 = redis.Redis(host=REDIS_HOST, port=6379)
    # print(msgpack.loads(r2.hget('dict_kangxi', '好')))

    def sub(word):
        definition = []
        _from = ""
        pinyin = ""
        val =  r2.hget('dict_kangxi', word)
        if val:
            kxword = msgpack.loads(val)
            _from = "康熙字典"
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
        return pinyin, definition, _from


    pinyin, definition, _from = sub(word)

    # 没有查到字典则使用对应正字重新查找
    if not pinyin:
        word2 = rm_variant(word)
        pinyin, definition, _from = sub(word2)
        if definition:
            definition = f'同{word2}<br>' + definition

    # 查拼音 TODO
    if not pinyin:
        _from = "unicode"
        val =  r2.hget('dict_unihan', word)
        if val:
            val = msgpack.loads(val)
            definition = val.get('kDefinition', '')
            pinyin = val.get('kMandarin', '')

    r2.close()
    return {'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}



if __name__ == "__main__":
    # main()
    test()
    import pprint
    # pprint.pprint(lookup('佛陀'))
    #pprint.pprint(lookup('𭮊'))
    #print(lookup('彌勒'))
    import pprint
    #pprint.pprint(lookinkangxi_pinyin('佛陀'))
    pprint.pprint(lookup('香'))
