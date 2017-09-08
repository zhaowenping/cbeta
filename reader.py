#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2017-09-08 18:46:59
from __future__ import unicode_literals, division, absolute_import, print_function

"""
web入口程序
"""

__all__ = []
__author__ = ""
__version__ = "0.0.1"


import os
from bottle import get, post
from bottle import route, run, static_file
from bottle import redirect, abort
from bottle import template
from bottle import jinja2_view as view
from bottle import request
from bottle import GeventServer

# from xsltproc import xsltproc, XSLT

# XSLT_FILE = 'static/tei.xsl'

@route('/')
def index():
    return 'Hello World!'

@route('/static/:filename')
def server_static(filename):
    return static_file(filename, root='static')

@route('/xml/:filename')
def server_xml(filename):
    return static_file(filename, root='xml')


def listdir():
    sutras = []
    for path in os.listdir('xml/{ye}'):
        if path.startswith(sutra):
            sutras.append(path)
    sutra.sort()

# 浏览器渲染，也可以
@route('/xml/:n')
#example: n = T01n0001_001
def browse(n):
    tt = XSLT(XSLT_FILE)
    XML_FILE = '../xml/%s/%s.xml' % (n[:3], n)
    if not os.path.exists(XML_FILE):
        abort(404, '无此文件')
    xhtml = tt.transform(XML_FILE)
    print(xhtml)
    #xhtml = xsltproc(XSLT_FILE, XML_FILE)
    return xhtml


# 显示菜单
sch_a = "menu/sutra_sch.lst"
sch_b = "menu/bulei_sutra_sch.lst"

@route('/mulu')
@view('temp/menu.jinja2')
def menu():
    menu = read_menu_file(sch_b)
    return {'menus': menu, 'request':request}


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
    return {'menus': menu, 'request':request, 'nav': nav}


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
# import psycopg2

# print(conn)
@get('/dict/:word')
def g_get(word):
    print('发过来一个字:%s' % word)
    pinyin = ''
    definition = ''
    with open('static/Unihan_Readings.txt') as fd:
        for line in fd:
            line = line.strip()
            if not line or line.startswith("#"): continue
            line = line.split(None, 2)
            unichar = 'U+%X' % ord(word)
            if unichar == line[0] and 'kDefinition' == line[1]:
                definition = line[2]
            if unichar == line[0] and 'kMandarin' == line[1]:
                pinyin = line[2]
                break

    print(pinyin, definition)

    return {'word': word, 'pinyin': pinyin, 'definition': definition}

@get('/gaiji')
@view('temp/gaiji.jinja2')
def dict_get():
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


# run(host = '0.0.0.0', port = 8081)
# GeventServer.run(host = '0.0.0.0', port = 8081)
run(host='0.0.0.0', port=8081, server='gunicorn', workers=4)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    #main()
    test()


