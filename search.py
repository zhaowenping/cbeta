#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-06-02 20:03:54
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



def fullsearch(sentence):
    '''全文搜索'''
    # sentence2 = sentence.replace(' ', '')
    url = "http://127.0.0.1:9200/cbeta/fulltext/_search?"#创建一个文档，如果该文件已经存在，则返回失败
    queryParams = "pretty&size=50"
    url = url + queryParams
    data = {
     "query": {
        "match": {
            "content": sentence,
        }
    },
    "highlight": {
        "fields": {
            "content": {

            }
        }
    }
}

    r = requests.get(url, json=data, timeout=10)
    hits = r.json()['hits']['hits']
    # result = []
    # for i  in hits:
    #     _source = i["_source"]
    #     author = _source['author'].split('\u3000')[0]
    #     juan = _source["filename"].split('n')[0]
    #     # result.append((''.join(i['highlight']['content']), f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}', _source['title'], author))
    #     if zi_order(sentence, _source['content']):
    #         result.append({'hl': highlight(sentence, _source['content']), 'an': f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}',
    #             'title':_source['title'], 'author': author, 'content': _source['content'],
    #             'filename': _source["filename"].split('.')[0]})

    # # sorted(result, key=lambda x: pagerank(x['filename']), reverse=True)
    # result.sort(key=lambda x: pagerank(x['filename']))  #, sentence, x['content']))
    #     # else:
    #     #     import pprint
    #     #     pprint.pprint(('||'.join(_source['content']), f'/xml/{juan}/{_source["filename"]}#{_source["pid"]}', _source['title'], author))

    return hits



if __name__ == "__main__":
    pprint.pprint(fullsearch('止觀明靜'))

