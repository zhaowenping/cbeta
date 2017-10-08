#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-10-08 13:25:18
from __future__ import unicode_literals, division, absolute_import, print_function

"""
web入口程序
"""

__all__ = []
__author__ = ""
__version__ = "0.0.1"


import os
import gzip
from bottle import get, post
from bottle import route, run, static_file, default_app
from bottle import redirect, abort
from bottle import template
from bottle import jinja2_view as view
from bottle import request
from bottle import GeventServer

# from xsltproc import xsltproc, XSLT

# XSLT_FILE = 'static/tei.xsl'

@route('/')
@view('temp/index.jinja2')
def index():
    return {'Hello World!':''}

@route('/static/:filename#.+#')
def server_static(filename):
    return static_file(filename, root='static')

@route('/xml/:filename#.+#')
def server_xml(filename):
    return static_file(filename, root='xml')


def listdir():
    sutras = []
    for path in os.listdir('xml/{ye}'):
        if path.startswith(sutra):
            sutras.append(path)
    sutra.sort()

# # 浏览器渲染，也可以
# @route('/xml/:n')
# #example: n = T01n0001_001
# def browse(n):
#     tt = XSLT(XSLT_FILE)
#     XML_FILE = '../xml/%s/%s.xml' % (n[:3], n)
#     if not os.path.exists(XML_FILE):
#         abort(404, '无此文件')
#     xhtml = tt.transform(XML_FILE)
#     print(xhtml)
#     #xhtml = xsltproc(XSLT_FILE, XML_FILE)
#     return xhtml
#

# 显示菜单
sch_a = "static/sutra_sch.lst"
sch_b = "static/bulei_sutra_sch.lst"

@route('/mulu')
@view('temp/menu.jinja2')
def menu():
    menu = read_menu_file(sch_b)
    return {'menus': menu, 'request':request, 'yiju': '部類'}

@route('/cebie')
@view('temp/menu.jinja2')
def menu():
    menu = read_menu_file(sch_a)
    return {'menus': menu, 'request':request, 'yiju': '冊別'}


@route('/mulu/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu(bulei):
    menu = read_menu_file(sch_b)
    bulei = bulei.split('/')

    nav = [('/mulu', '总目录')]
    for b in bulei:
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        sutra = bulei[-1].split()[0]  # T01n0002
        ye = sutra.split('n')[0]
        # 查找第一卷(有些不是从第一卷开始的)
        sutras = []
        for path in os.listdir('xml/{ye}'.format(**locals())):
            if path.startswith(sutra):
                sutras.append(path)
        sutras.sort()
        sutra = sutras[0]            # T01n0002_001.xml
        # url = f"http://10.81.25.167:8080/xml/{ye}/{sutra}"
        url = f"/xml/{ye}/{sutra}"
        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '部類'}

@route('/cebie/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu(bulei):
    menu = read_menu_file(sch_a)
    bulei = bulei.split('/')

    nav = [('/cebie', '总目录')]
    for b in bulei:
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        sutra = bulei[-1].split()[0]  # T01n0002
        ye = sutra.split('n')[0]
        # 查找第一卷(有些不是从第一卷开始的)
        sutras = []
        for path in os.listdir('xml/{ye}'.format(**locals())):
            if path.startswith(sutra):
                sutras.append(path)
        sutras.sort()
        sutra = sutras[0]            # T01n0002_001.xml
        # url = f"http://10.81.25.167:8080/xml/{ye}/{sutra}"
        url = f"/xml/{ye}/{sutra}"
        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '冊別'}


# 处理搜索
@get('/search')
@view('temp/search.jinja2')
def search():
    return {}

# 搜索！
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *
import opencc

import time
import pprint

# ix = open_dir("index")
# 搜索content内容
# qp = QueryParser("content", ix.schema)

# TODO 搜索的时候被搜索内容应该手动分词
@post('/search')
@view('temp/search.jinja2')
def search_post():
    global qp
    # content = request.forms.get('content')
    # content = request.POST.get('content')
    print(request.POST)
    content = request.forms.content
    print(('content', content))
    content = opencc.convert(content, config='s2t.json')
    # content = request.forms.getunicode('content')
    # print(('content', content))
    mq = qp.parse(content)
    print(mq)
    # mq = Term('content', content)
    xx = []
    s = time.time()
    print('----------------------------------------')
    with ix.searcher() as searcher:
        # results = searcher.search(mq)
        pageid = 1
        results = searcher.search_page(mq, pageid, pagelen=20)
        # results = searcher.find(mq)
        found = results.scored_length()
        print(('found:', found))

        for hit in results:
            hl = hit.highlights("content",  top=5)
            ct = hit["content"]
            juan = hit["filename"].split('n')[0]
            an = f'/xml/{juan}/{hit["filename"]}#{hit["p"]}'
            xx.append((hl, an, hit['title']))
            pprint.pprint((hl, an))
    e = time.time()

    print('----------------------------------------')
    print('搜索花费时间:%d' % (e-s))
    print(xx)
    return {'results': xx}

# "menu/sutra_sch.lst"
# "menu/bulei_sutra_sch.lst'

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

# 处理组合字
import psycopg2
import json
import time

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
with open('dict/dfb.json') as fd:
    dfb = json.load(fd)
e = time.time()
print('装入丁福宝词典，用时%s' % (e - s))

s = time.time()
with open('dict/庄春江汉译阿含经词典ver4.json') as fd:
    ccc = json.load(fd)
e = time.time()
print('装入庄春江词典，用时%s' % (e - s))

s = time.time()
with open('dict/nsl.json') as fd:
    nsl = json.load(fd)
e = time.time()
print('装入南山律学词典，用时%s' % (e - s))

s = time.time()
with open('dict/cxy.json') as fd:
    cxy = json.load(fd)
e = time.time()
print('装入佛學常見詞彙（陳義孝），用时%s' % (e - s))

s = time.time()
with open('dict/于凌波唯识名词白话新解.json') as fd:
    ylb = json.load(fd)
e = time.time()

print('装入于凌波唯识名词白话新解，用时%s' % (e - s))



# print(conn)
@get('/dict/:word')
def dict_get(word):
    '''查字典'''
    print('发过来一个字:%s' % word)
    pinyin = ''
    _from = ''
    definition = ''
    if len(word) == 1:
        if word in kangxi:
            _from = "康熙字典"
            definition = []
            if "說文解字" in kangxi[word]:
                definition.append(kangxi[word]["說文解字"])
            if "康熙字典" in kangxi[word]:
                definition.append(kangxi[word]["康熙字典"])
            if "宋本廣韻" in kangxi[word]:
                definition.append(kangxi[word]["宋本廣韻"])
            if definition:
                definition = '|'.join(definition)
            elif '英文翻譯' in kangxi[word]:
                definition = kangxi[word]['英文翻譯']
            else:
                definition = ''
        else:
            _from = "unicode"
            definition = unihan.get(word, {}).get('kDefinition', '')
            pinyin = unihan.get(word, {}).get('kMandarin', '')
    elif word in fk:
        _from = "佛光山"
        definition = fk[word]
    elif word in dfb:
        _from = dfb[word][0]['usg']
        definition = dfb[word][0]['def']
    elif word in ccc:
        _from = "庄春江"
        definition = ccc[word]
    elif word in nsl:
        _from = "南山律"
        definition = nsl[word]
    elif word in cxy:
        _from = "陈孝义"
        definition = nsl[word]
    elif word in ylb:
        _from = "于凌波"
        definition = ylb[word]

    if _from:
        pinyin = ' '.join([unihan.get(x, {}).get('kMandarin', ' ') for x in word])
    # print(pinyin, definition)

    return {'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}

@get('/gaiji')
@view('temp/gaiji.jinja2')
def g_get():
    q = request.GET.q
    print(q)
    conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    if q:
        if len(q) > 1:
            cur.execute('select * from cb where position(%s in des)>0 or position(%s in name)>0', (q, q))
        else:
            cur.execute('select * from cb where nor = %s or val = %s or position(%s in des)>0', (q, q, q))
    else:
        cur.execute('select * from cb where nor is null or val is null')
    data = cur.fetchall()
    result = []
    for i in data:
    #     print(i)
        name = i[0]
        nor = i[1]
        val = i[2]
        des = i[3]
        uni = i[4]
        pua = i[5]
        tag = i[6]
        result.append((name, nor, val, des, uni, pua, tag))

    conn.commit()
    cur.close()
    conn.close()

    return {'result': result}

import urllib.request
@post('/gaiji')
@view('temp/gaiji.htm')
def gaiji_post():
    print('~~~~~~~~~~~~~~~~~~~~~')
    name = request.forms.name
    if not name:
        return {}
    val = request.forms.val
    norm = request.forms.norm
    q = val
    if not val:
        val = None
        q = norm

    if not norm:
        norm = None
    print((name, val, norm))
    conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute('update cb set nor = %s, val = %s, tag = %s where name = %s', (norm, val, True, name))
    conn.commit()
    cur.close()
    conn.close()
    print('____________________________')
    redirect('/gaiji?q=%s'%urllib.request.quote(q))


@get('/sd')
@view('temp/sd.jinja2')
def gaiji_sd_get():
    print('查询sd')
    q = request.GET.q
    conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    if q:
        cur.execute('select name, romanu, romanc, value, siddham_font from siddham where position(%s in romanu)>0 or position(%s in romanc)>0 order by name', (q, q))
    else:
        cur.execute('select name, romanu, romanc, value, siddham_font from siddham order by name')
        # cur.execute("select name, romanu, romanc, value from siddham where romanc ='' or romanu = '' order by name")
        # cur.execute("select name, romanu, romanc, value from siddham where value is not null order by name")
    data = cur.fetchall()
    result = []
    for i in data:
    #     print(i)
        name = i[0].strip()
        romanu = i[1].strip()
        romanc = i[2].strip()
        value = i[3].strip() if i[3] else ''
        sd = i[4].strip() if i[4] else ''
        tt = name[19:].strip()
        url = '/static/sd-gif/{}/SD-{}.gif'.format(tt[:2], tt)
        result.append((name, romanu, romanc, value, sd, url))
    print(result)
    print('____________________________')
    conn.commit()
    cur.close()
    conn.close()
    return {'result': result}

@post('/sd')
@view('temp/sd.htm')
def gaiji_sd_post():
    print('~~~~~~~~~~~~~~~~~~~~~')
    name = request.forms.name
    if not name:
        return {}
    val = request.forms.val
    if not val:
        val = None

    print((name, val))
    conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute('update siddham set value = %s where name = %s', (val, name))
    conn.commit()
    cur.close()
    conn.close()
    print('____________________________')
    redirect('/sd?q=%s'%urllib.request.quote(val))


# GeventServer.run(host = '0.0.0.0', port = 8081)
app = default_app()
# run(host='0.0.0.0', port=8081, server='gunicorn', workers=4)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    #main()
    test()
    run(host = '0.0.0.0', port = 8081)


