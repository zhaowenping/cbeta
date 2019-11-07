#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2019-11-07 02:59:22
from __future__ import unicode_literals, division, absolute_import, print_function

"""
web入口程序
"""

__all__ = []
__author__ = ""
__version__ = "0.0.1"


import re
import os
import gzip
import json
import time
import datetime

from bottle import get, post, response
from bottle import route, run, static_file, default_app
from bottle import redirect, abort
from bottle import Jinja2Template as template
from bottle import jinja2_view as view
from bottle import request
from bottle import GeventServer

# from whoosh.index import open_dir
# from whoosh.qparser import QueryParser
# from whoosh.query import *
# import psycopg2
# import opencc
import jieba

import pprint
from libhan import hk2iast, read_menu_file, HKdict2iast
from libhan import get_all_juan
from libhan import Search
from libhan import TSDetect
from libhan import convert2t
from libhan import convert2s
from libhan import normyitizi
from libhan import fullsearch
from libhan import rm_ditto_mark
from libhan import make_url

from libhan import lookup, lookinkangxi, lookinsa, zhuyin
from libhan import unihan
from libhan import get_prev_juan, get_next_juan

# from xsltproc import xsltproc, XSLT

# XSLT_FILE = 'static/tei.xsl'

@route('/')
@view('temp/index.html')
def index():
    return {'Hello World!':''}

@get('/tools')
@view('temp/tools.jinja2')
def tools_get():
    return {}


@route('/zhouyu/:filename#.+#')
def server_zhouyu(filename):
    return static_file(filename, root='zhouyu')

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

# 跳转上一卷/下一卷
@route('/prev/:sutra')
def getf_prev_juan(sutra):
    sutra = get_prev_juan(sutra)
    book = sutra.split('n')[0]
    url = f"/xml/{book}/{sutra}.xml"  # T01n0002_001.xml
    redirect(url)

@route('/next/:sutra')
def getf_next_juan(sutra):
    sutra = get_next_juan(sutra)
    book = sutra.split('n')[0]
    url = f"/xml/{book}/{sutra}.xml"  # T01n0002_001.xml
    redirect(url)

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
sch_a = read_menu_file("static/sutra_sch.lst")
sch_b = read_menu_file("static/bulei_sutra_sch.lst")
sch_dzyz = read_menu_file("static/dzyz.lst")
sch_fyjs = read_menu_file("static/fyjs.lst")
sch_pali = read_menu_file("static/pali.lst")
sch_san = read_menu_file("static/san.lst")

@route('/mulu')
@view('temp/menu.jinja2')
def menu1():
    return {'menus': sch_b, 'request':request, 'yiju': '大正藏部類'}

@route('/cebie')
@view('temp/menu.jinja2')
def menu2():
    return {'menus': sch_a, 'request':request, 'yiju': '大正藏冊別'}

@route('/dzyz')
@view('temp/menu.jinja2')
def menu3():
    return {'menus': sch_dzyz, 'request':request, 'yiju': '大衆閲藏5.4版'}

@route('/fyjs')
@view('temp/menu.jinja2')
def menu4():
    return {'menus': sch_fyjs, 'request':request, 'yiju': '大德長老目錄'}

@route('/palimulu')
@view('temp/menu.jinja2')
def menu5():
    return {'menus': sch_pali, 'request':request, 'yiju': '巴利三藏(CST4)'}

@route('/sanskrit')
@view('temp/menu.jinja2')
def menu6():
    return {'menus': sch_san, 'request':request, 'yiju': '梵文三藏(DSBC)'}

@route('/mulu/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu1(bulei):
    menu = sch_b
    bulei = bulei.split('/')
    root = '/mulu'

    nav = [(root, '总目录')]
    for b in bulei:
        if b not in menu: abort(404)
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        sutra = bulei[-1].split()[0]  # T01n0002
        zang = sutra.split('n')[0]              # T01
        juan = get_all_juan(sutra)[0]           # 001
        url = f"/xml/{zang}/{sutra}_{juan}.xml"  # T01n0002_001.xml
        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '大正藏部類', 'root':root}

@route('/cebie/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu2(bulei):
    menu = (sch_a)
    bulei = bulei.split('/')
    root = '/cebie'

    nav = [(root, '总目录')]
    for b in bulei:
        if b not in menu: abort(404)
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        sutra = bulei[-1].split()[0]  # T01n0002
        zang = sutra.split('n')[0]              # T01
        if '_' in sutra:
            sutra, juan = sutra.split('_')
        else:
            # 查找第一卷(有些不是从第一卷开始的)
            juan = get_all_juan(sutra)              # 001
            if not juan:
                abort(404, f'没找到文件: /xml/{zang}/{sutra}_*.xml')
            juan = juan[0]
        url = f"/xml/{zang}/{sutra}_{juan}.xml"  # T01n0002_001.xml
        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '大正藏冊別', 'root': root}


@route('/dzyz/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu3(bulei):
    menu = sch_dzyz
    bulei = bulei.split('/')
    root = '/dzyz'

    nav = [(root, '总目录')]
    for b in bulei:
        if b not in menu: abort(404)
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        sutra = bulei[-1].split()[0]  # T01n0002
        zang = sutra.split('n')[0]              # T01
        juan = get_all_juan(sutra)[0]           # 001
        url = f"/xml/{zang}/{sutra}_{juan}.xml"  # T01n0002_001.xml
        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '大衆閲藏5.4版', 'root':root}

@route('/fyjs/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu4(bulei):
    menu = sch_fyjs
    bulei = bulei.split('/')
    root = '/fyjs'

    nav = [(root, '总目录')]
    for b in bulei:
        if b not in menu: abort(404)
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        sutra = bulei[-1].split()[0]  # T01n0002
        zang = sutra.split('n')[0]              # T01

        if '_' in sutra:
            sutra, juan = sutra.split('_')
        else:
            # 查找第一卷(有些不是从第一卷开始的)
            juan = get_all_juan(sutra)              # 001
            if not juan:
                abort(404, f'没找到文件: /xml/{zang}/{sutra}_*.xml')
            juan = juan[0]

        if '#' in juan:
            juan, para = sutra.split('#')
            url = f"/xml/{zang}/{sutra}_{juan}.xml#{para}"  # T01n0002_001.xml
        else:
            url = f"/xml/{zang}/{sutra}_{juan}.xml"  # T01n0002_001.xml

        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '大德長老居士推薦目錄', 'root':root}


@route('/palimulu/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu5(bulei):
    menu = sch_pali
    bulei = bulei.split('/')
    root = '/palimulu'

    nav = [(root, '总目录')]
    for b in bulei:
        if b not in menu: abort(404)
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        src, text = bulei[-1].split(maxsplit=1)  # T01n0002

        if '_' in src:
            src = src.replace('_', '/')
            url = f"/xml/cscd/{src}.xml"  # T01n0002_001.xml
        else:
            url = f"/xml/cscd/tipitaka/{src}.xml"  # T01n0002_001.xml

        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '巴利三藏目錄', 'root':root}


@route('/sanskrit/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu6(bulei):
    menu = sch_san
    bulei = bulei.split('/')
    root = '/sanskrit'

    nav = [(root, '总目录')]
    for b in bulei:
        if b not in menu: abort(404)
        menu = menu[b]
        t = '/'.join((nav[-1][0], b))
        nav.append((t, b))
    nav.pop(0)

    # 跳转到正文
    if not menu:
        src, text = bulei[-1].split(maxsplit=1)  # T01n0002

        if '_' in src:
            src = src.replace('_', '/')
            url = f"/xml/cscd/{src}.xml"  # T01n0002_001.xml
        else:
            url = f"/xml/cscd/tipitaka/{src}.xml"  # T01n0002_001.xml

        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '梵文三藏目錄', 'root':root}


# 处理搜索

ss = Search()
ts = TSDetect()

@get('/jt2ft')
def jiantifanti():
    content = request.GET.content
    if ts.detect(content)['confidence'] == 's':
        content = convert2t(content)
    return {'content': content}

@get('/searchmulu')
@post('/searchmulu')
@view('temp/search.jinja2')
def searchmulu():
    '''搜索标题, GET方法为目录部典籍查找所用'''
    if request.method == "GET":
        title = request.GET.title
        # 去除HTML标签、注释、卷数, 留下标题
        title = re.sub(r'<.*?>', '', title)  # title=[34]<span style="color:red">阿</span>差末菩薩經
        title = re.sub(r'\(.*?\)', '', title)
        title = re.sub(r'\[\w*?\]', '', title)
        title = re.sub(r'[一二三四五六七八九十百]+卷', '', title)
    else:
        title = request.forms.content
    # 使用经号方式查找藏经
    an = make_url(title)
    if an:
        redirect(an)

    if ts.detect(title)['confidence'] == 's':
        # title = opencc.convert(title, config='s2t.json')
        title = convert2t(title)
    results = []
    if not title:
        return {'results': results}
    # TODO:搜索t1000, t1000_001, T01n0001, T01n0001_001, T01n0001_p0001a01, T01,no.1,p.1a1
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

# 搜索！

# ix = open_dir("index")
# 搜索content内容
# qp = QueryParser("content", ix.schema)

# TODO 搜索的时候被搜索内容应该手动分词
@get('/search')
@view('temp/search.jinja2')
def search_post():
    # global qp
    # print(request.POST)
    content = request.GET.content
    if not content: return {}
    # content = request.forms.content
    if ts.detect(content)['confidence'] == 's':
        content = convert2t(content)
    content = normyitizi(content)
    # stop_words = frozenset("不無一是有之者如法為故生此佛所三以二人云也於中若得心大")
    # content = ''.join(set(content)-stop_words)
    print(('content', content))
    s = time.time()
    xx = fullsearch(content)
    # mq = qp.parse(content)
    # print(mq)
    # # mq = Term('content', content)
    # xx = []
    # print('----------------------------------------')
    # with ix.searcher() as searcher:
    #     # results = searcher.search(mq)
    #     pageid = 1
    #     results = searcher.search_page(mq, pageid, pagelen=40)
    #     # results = searcher.find(mq)
    #     found = results.scored_length()
    #     print(('found:', found))

    #     for hit in results:
    #         hl = hit.highlights("content",  top=5)
    #         ct = hit["content"]
    #         juan = hit["filename"].split('n')[0]
    #         an = f'/xml/{juan}/{hit["filename"]}#{hit["p"]}'
    #         xx.append((hl, an, hit['title']))
    #         pprint.pprint((hl, an))
    e = time.time()

    print('----------------------------------------')
    print('搜索花费时间:%d' % (e-s))
    print(xx)

    with open('search.dict', 'a+') as fd:
        fd.write(datetime.datetime.now().strftime("%Y%m%dT%T ") + content + '\n')

    return {'results': xx}

# "menu/sutra_sch.lst"
# "menu/bulei_sutra_sch.lst'

# print(conn)
@get('/dict/ccc/:word')
def ccc_dict_get(word):
    pinyin = ''
    _from = ''
    definition = ''
    if word in ccc:
        _from = "庄春江"
        definition = ccc[word]
    return json.dumps({'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}, ensure_ascii=False, indent =4)

@get('/dict/dfb/:word')
def dfb_dict_get(word):
    pinyin = ''
    definition = ''
    if word in dfb:
        definition = dfb[word]
    return json.dumps({'word': word, 'pinyin': pinyin, 'definition': definition}, ensure_ascii=False, indent =4)

@get('/dict/yph')
@view('temp/dict.jinja2')
def fxcd_dict_all():
    return {'dd': fxcd}

@get('/dict/fxcd/:word')
# @view('temp/search.jinja2')
def fxcd_dict_get(word):
    pinyin = ''
    _from = ''
    definition = ''
    print(word)
    if word in fxcd:
        _from = "於沛煌"
        definition = fxcd[word]
    return json.dumps({'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}, ensure_ascii=False, indent =4)

@get('/dict/fk/:word')
def fk_dict_get(word):
    pinyin = ''
    _from = ''
    definition = ''
    if word in fk:
        _from = "佛光山"
        definition = fk[word]
    return json.dumps({'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}, ensure_ascii=False, indent =4)

@get('/dict/kx/:word')
def kx_dict_get(word):
    pinyin = ''
    _from = ''
    definition = ''
    # {'word': word, 'pinyin': pinyin, 'def': definition, 'from': _from}
    # lookinkangxi(word)
    if len(word) == 1:
        if word in kangxi:
            _from = "康熙字典"
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
        else:
            kxword = None
    return json.dumps({word: kxword}, ensure_ascii=False, indent =4)
    # return json.dumps({'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}, ensure_ascii=False, indent =4)

@get('/dict/:word')
def dict_get(word):
    '''查字典'''
    pt = re.compile(r'\[|\]|\d')  # 应该在前端过滤
    word = pt.sub('', word)
    # word = re.sub(r'\[\d*\]', '', word)
    print('发过来一个字:%s' % word)
    pinyin = ''
    _from = ''
    definition = ''

    if len(word) != 1:
        rr = lookup(word)
        _from = rr['from']
        definition = rr['definition']
        print(definition)

    if len(word) == 1:
        result = lookinkangxi(word)
        _from = result['from']
        if definition:
            definition = '<br>'.join((definition, result['def']))
        else:
            definition = result['def']
        pinyin = result['pinyin']

    if not _from:
        result = lookinsa(word)
        _from = result['from']
        definition = result['def']
        pinyin = result['pinyin']

    # 用Unicode数据库注音
    if _from and not pinyin:
        pinyin = [unihan.get(x, {}).get('kMandarin', '') for x in word]
        pinyin = ' '.join([x.split()[0] if x else '' for x in pinyin])

    with open('yoga.dict', 'a+') as fd:
        fd.write(datetime.datetime.now().strftime("%Y%m%dT%T ") + word + '\n')

    print({'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from})
    return json.dumps({'word': word, 'pinyin': pinyin, 'definition': definition, 'from': _from}, ensure_ascii=False, indent =4)

@get('/gaiji')
@view('temp/gaiji.jinja2')
def g_get():
    q = request.GET.q
    print(q)
    conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    if q:
        if len(q) > 1:
            cur.execute('select * from cb where position(%s in des)>0 or position(%s in name)>0 order by cipin desc', (q, q))
        else:
            cur.execute('select * from cb where nor = %s or val = %s or position(%s in des)>0 order by cipin desc', (q, q, q))
    else:
        # cur.execute('select * from cb where nor is null or val is null order by cipin desc')
        cur.execute('select * from cb where nor is null and val is null  and info is not null order by cipin desc')
    data = cur.fetchall()
    result = []
    for i in data:
    #     print(i)
        name = i[0]
        nor = i[1]
        val = i[2]
        des = i[3]
        uni = i[4]
        tag = i[5]
        nun = i[6]
        info = i[7]
        cipin = i[8]
        # result.append((name, nor, val, des, uni, pua, tag, info))
        result.append((name, nor, val, des, uni, tag, info, cipin))

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

# xml/T13/T13n0423_001.xml
@route('/zh/:filename#.+#')
def zh(filename):
    '''简体版'''
    print('简体版本', filename)
    with open(filename) as fd:
        content = fd.read()
    # 修改语言为简体
    # content = content.replace('xml:lang="lzh-Hant"', 'xml:lang="lzh-Hans"')
    content = content.replace('Hant', 'Hans')
    # 添加敬语染色 honorific  如來、應供、正遍知、明行足、善逝、世間解、無上士、調御丈夫、天人師、佛、世尊
    honorific = {'多陀怛伽度', '多陀竭', '多陀阿伽[度陀馱]', '如來', '怛他蘗多夜?', '怛薩阿竭', '怛闥阿竭', '陀多竭多',
            '阿羅訶', '阿羅呵', '(?:三藐三)?佛陀?', '三耶三佛檀?', # '三藐三佛陀', '三耶三佛', '三耶三佛檀',
                 '正[徧遍][知覺]', '等正覺', '三藐三菩陀',
                 '如來', '應供', '正遍知', '明行足', '善逝', '世間解', '無上士', '調御丈夫', '天人師', '世尊', '薄伽梵', '婆伽婆', }
    # content = re.sub(r'(?!辟支|仿)(佛陀?)', r'<persName>\1</persName>', content)
    honorific = '|'.join(sorted(honorific, key=len, reverse=True))
    # print(honorific)
    content = re.sub(f'({honorific})', r'<persName>\1</persName>', content)
    # 简体繁体双引号, 单引号切换
    content = content.translate({0x300c: 0x201c, 0x300d: 0x201d, 0x300e: 0x2018, 0x300f: 0x2019})
    # content = opencc.convert(content, config='t2s.json')
    content = rm_ditto_mark(content)
    content = convert2s(content)
    print(filename)
    response.content_type = 'text/xml'
    return content

@get('/t2s')
def t2s_get():
    '''繁体转简体'''
    return static_file('t2s.htm', root='static')

@post('/t2s')
def t2s_post():
    '''繁体转简体'''
    tcontent = json.loads(request.forms.text).get('text', '')
    # 去除行间注释
    tcontent = re.sub(r'\[\w*?\]|\[\*\]', '', tcontent)
    # 去除组字式
    # conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="127.0.0.1", port="5432")
    # cur = conn.cursor()
    # for zuzishi in re.findall(r'\[[^\[\]]*?\]', tcontent):
    #     cur.execute("select uni, nu, nor from cb2 where des='%s'", (zuzishi,))
    #     data = cur.fetchone()
    #     zi = data[0] or data[1] or data[2]
    #     if zi:
    #         tcontent = tcontent.replace(zuzishi, zi)
    # conn.commit()
    # cur.close()
    # conn.close()

    # 去除重复符号
    scontent = rm_ditto_mark(tcontent)
    scontent = convert2s(scontent)
    with open('t2s.txt', 'a+') as fd:
        fd.write(tcontent)
        fd.write('\n--------------------\n')

    response.content_type = 'application/json'
    return {"tcontent": tcontent, "scontent": scontent}

@route('/zh_TW/:filename#.+#')
def zh_TW(filename):
    '''正字版'''
    print('正字版本', filename)
    with open(filename) as fd:
        content = fd.read()
    # 修改语言为简体
    # content = content.replace('Hant', 'Hans')
    # 添加敬语染色 honorific  如來、應供、正遍知、明行足、善逝、世間解、無上士調御丈夫、天人師、佛、世尊
    honorific = {'如來', '多陀怛伽度', '多陀竭', '多陀阿伽[度陀馱駄多]', '怛他蘗多夜?', '怛薩阿竭', '怛闥阿竭', '陀多竭多', '多陀阿加度',
            '應供', '阿羅訶', '阿羅呵', '至真', '阿囉訶',
            '正遍知', '正[徧遍][知覺]', '等正覺', '三藐三菩陀', '正等覺', '平等正覺', '正遍智', '正徧知', '正遍覺', '正真道', '正等覺', '正等正覺', '正覺等',
               '三藐三佛', '三藐三佛陀', '三耶三佛', '三耶三佛檀', '阿耨多羅三耶三佛', '三耶三菩',
            '明行足', '明行成為', '明行具足', '明行圓滿', '通行備足',
            '善逝', '修伽陀', '脩伽陀', '蘇揭多', '修伽多', '脩伽度', '脩伽多',
            '世間解', '路迦憊',
            '無上士調御丈夫', '無上丈夫調御士', '無上調御丈夫', '無上士道法御', '無上法御',
            '天人師', '天人之師', '舍多提婆魔㝹舍喃', '舍多提波□魔㝹舍南', '舍多提婆摩㝹舍喃', '舍多提婆魔菟舍喃', '舍多提婆摩嵬舍喃', '天人教師',
            '佛陀', '佛馱', '浮陀', '浮頭', '沒馱', '步他', '馞陀', '復豆', '浮屠', '浮圖',
            '世尊', '薄伽梵', '婆伽婆'}
    # content = re.sub(r'(?!辟支|仿)(佛陀?)', r'<persName>\1</persName>', content)
    honorific = '|'.join(sorted(honorific, key=len, reverse=True))
    # print(honorific)
    content = re.sub(f'({honorific})', r'<persName>\1</persName>', content)
    # 简体繁体双引号, 单引号切换
    # content = content.translate({0x300c: 0x201c, 0x300d: 0x201d, 0x300e: 0x2018, 0x300f: 0x2019})
    # content = opencc.convert(content, config='t2s.json')
    content = normyitizi(content)
    content = rm_ditto_mark(content)
    print(filename)
    response.content_type = 'text/xml'
    return content


@route('/zhx/:filename')
def zhx(filename):
    '''从目录简体版转到简体阅读章节'''
    jing = filename.split()[0]
    zang = jing.split('n')[0]
    juan = get_all_juan(jing)[0]
    url = f"/zh/xml/{zang}/{jing}_{juan}.xml"
    redirect(url)


# 输出pdf
# import xhtml2pdf.pisa as pisa
# from StringIO import StringIO

@route('/download', methods=['GET'])
def download_pdf():
    env = Environment(loader=PackageLoader(current_app.name, 'templates'))
    template = env.get_template('test.jinja2') # 获得页面模板

    html = template.render(name='大Ren', font_path='/static/simsun.ttf').encode('utf-8')
    result = StringIO()
    pdf = pisa.CreatePDF(StringIO(html), result)
    resp = make_response(result.getvalue())
    resp.headers["Content-Disposition"] = ("attachment; filename='{0}'; filename*=UTF-8''{0}".format('test.pdf'))
    resp.headers['Content-Type'] = 'application/pdf'
    return resp

# 异体字检索
@get('/yitizi/:qu')
@view('temp/yitizi.jinja2')
def yitizi_get(qu):
    with gzip.open(f'dict/yitizi{qu}.json.gz') as fd:
        yitizi = json.load(fd)
    result = []
    for no in yitizi:
        rzi = yitizi[no][0]
        #if len(yitizi[no]) > 1:
        ozi = yitizi[no][1:]
        #else:
        #    ozi = []
        result.append((no, rzi, ozi))
    return {'result': result}

@get('/ytz')
@view('temp/ytz.jinja2')
def ytz():
    result = []
    return {'result': result}
    with open('dict/ytzb.txt') as fd:
        for line in fd:
            line = line.strip()
            line = line.split()
            result.append((line[0], line[1:]))

    return {'result': result}

punct = re.compile(r"([\u3000-\u303f\ufe10-\uff0f\uff1a-\uffee])")

from libhan import diff_ctx

@get('/diff')
@view('temp/diff.jinja2')
def diff_get():

    try:
        with open('lfile.tmp') as fd:
            lfile = fd.read()

        with open('rfile.tmp') as fd:
            rfile = fd.read()

        return diff_ctx(lfile, rfile)

    except:
        return {}


import chardet
# chardet.detect(r.content)['encoding']

@post('/diff')
@view('temp/diff.jinja2')
def diff_post():
    '''比较两个文件不同'''
    lfile = request.files.lfile
    rfile = request.files.rfile

    # 自动编码检测
    lfile = lfile.file.read() #.decode('utf8')
    encoding = chardet.detect(lfile)['encoding']
    if encoding.startswith('GB'):
        encoding = 'GB18030'
    lfile = lfile.decode(encoding, 'replace')
    # print(request.forms.punct)
    # print(request.forms.punct == 'true')
    if request.forms.punct == 'true':
        lfile = punct.sub('', lfile)
    with open('lfile.tmp', 'w') as fd:
        fd.write(lfile)

    rfile = rfile.file.read() #.decode('utf8')
    encoding = chardet.detect(rfile)['encoding']
    if encoding.startswith('GB'):
        encoding = 'GB18030'
    rfile = rfile.decode(encoding, 'replace')
    if request.forms.punct == 'true':
        rfile = punct.sub('', rfile)
    with open('rfile.tmp', 'w') as fd:
        fd.write(rfile)

    redirect(f'/diff')


# jieba.load_userdict('dict/terms.txt')
@get('/diff/word')
@view('temp/diff.jinja2')
def diff_word_get():
    '''按照词比较两个文件不同'''
    with open('lfile.tmp') as fd:
        lfile = fd.read()
        lfile = list(jieba.cut(lfile))

    with open('rfile.tmp') as fd:
        rfile = fd.read()
        rfile = list(jieba.cut(rfile))

    return diff_ctx(lfile, rfile)

@get('/diff/line')
@view('temp/diff.jinja2')
def diff_line_get():
    '''按照行比较两个文件不同'''
    with open('lfile.tmp') as fd:
        lfile = fd.read()
        lfiles = [line.strip() for line in lfile.splitlines()]

    with open('rfile.tmp') as fd:
        rfile = fd.read()
        rfiles = [line.strip() for line in rfile.splitlines()]

    return diff_ctx(lfile, rfile)


# xml/T13/T13n0423_001.xml
@get('/dharani/:filename#.+#')
@view('temp/dharani.jinja2')
def dharani_get(filename):
    '''咒语标注计划'''
    print(f'zhouyu/{filename}')
    if os.path.exists(f'zhouyu/{filename}'):
        print('新版本')
        filename = f'zhouyu/{filename}'
        with open(filename) as fd:
            content = fd.read()
    else:
        print('旧版本')
        with open(filename) as fd:
            content = fd.read()
    content = content.replace("&", "&amp;")
    content = content.replace("<", "&lt;")
    content = content.replace(">", "&gt;")
    content = content.replace('"', "&quot;")
    content = content.replace("'", "&apos;")
    # response.content_type = 'text/xml'
    # content = opencc.convert(content, config='t2s.json')
    return {"content": content, "path": filename}

import bottle
bottle.BaseRequest.MEMFILE_MAX = 24 * 1024 * 1024 # (or whatever you want)
@post('/dharani')
def dharani_post():
    '''咒语标注计划: 保存修改后的文件'''
    xmlfile = request.forms.xmlfile
    path = request.forms.path
    ddir = os.path.split(path)[0]
    if not os.path.exists(f'zhouyu/{ddir}'):
        os.mkdir(f'zhouyu/{ddir}')
    with open(f'zhouyu/{path}', 'w') as fd:
        fd.write(xmlfile)
    # print(xmlfile)
    print(path)   # xml/X23/X23n0438_004.xml
    redirect(f'/dharani/{path}')

@get('/timeline')
@view('temp/timeline.jinja2')
def timeline_get():
    print('timeline')
    return {}

# 多音字处理
@get('/duoyinzi')
@view('temp/duoyinzi.jinja2')
def duoyinzi_get():
    with gzip.open('dict/duoyinzi.json.gz') as fd:
        data = json.load(fd)
    return {'result': data}

@post('/duoyinzi')
def duoyinzi_post():
    name = request.forms.name
    val = request.forms.val
    val = val.replace(r"[", " ").replace(r"]", " ").replace(r"'", "").replace(',', ' ')
    print(name, val, val.split())
    with gzip.open('dict/duoyinzi.json.gz') as fd:
        data = json.load(fd)

    if name in data:
        x = data[name]
        data[name] = x[0], x[1], val
    with gzip.open('dict/duoyinzi.json.gz', 'w') as fd:
        json.dump(data, fd, ensure_ascii=False)
    redirect(f'/duoyinzi')

# 词频
# 可疑发音校对
@get('/keyifayin')
@view('temp/keyifayin.jinja2')
def keyifayin_get():
    conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="kepan.org", port="5432")
    cur = conn.cursor()
    cur.execute('select * from keyifayin order by cipin desc')
    data = cur.fetchall()
    result = [i for i in data]
    conn.commit()
    cur.close()
    conn.close()
    return {'result': result}


@post('/keyifayin')
def keyifayin_post():
    zi = request.forms.name
    val = request.forms.val
    reason = request.forms.reason
    conn = psycopg2.connect(database="buddha", user="postgres", password="1234", host="kepan.org", port="5432")
    cur = conn.cursor()
    cur.execute('update keyifayin set cur = %s, tag = %s, reason=%s where zi = %s', (val, True, reason, zi))
    conn.commit()
    cur.close()
    conn.close()
    redirect(f'/keyifayin')

@get('/page')
def page_get():
    return []

# 法相词典
@get('/fxcd/:page')
@view('temp/dict.jinja2')
def new_dict1(page):
    q = request.GET.q
    pp = int(request.GET.pp or 800)  # 每頁詞條數量
    cp = min(int(request.GET.cp or 500), 500000) # 注音詞頻, 默認50, 最大不超過50萬
    page = int(page)
    with gzip.open('dict/fxcd.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: data[item].split('\n')[1:] for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, data[item].split('\n')[1:]) for item in data]
        # fxcd = [((item, zhuyin(item)), data[item].split('\n')[1:]) for item in data]
        fxcd = [((item, zhuyin(item)), (zhuyin(i, True, cp) for i in data[item].split('\n')[1:])) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 佛光山词典
@get('/fk/:page')
@view('temp/dict.jinja2')
def new_dict2(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/fk.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ' '.join(lookinkangxi(i)['pinyin'].split(' ')[0] for i in item)), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}


# 南山律学词典
@get('/nvd/:page')
@view('temp/dict.jinja2')
def new_dict3(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/nvd.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ' '.join(lookinkangxi(i)['pinyin'].split(' ')[0] for i in item)), (data[item],)) for item in data]
        total = len(fxcd)
        page = int(page)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 佛學常見詞彙（陳義孝)
@get('/cyx/:page')
@view('temp/dict.jinja2')
def new_dict4(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with open('dict/cyx.json') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    title = header['title']
    author = header['author']
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ' '.join(lookinkangxi(i)['pinyin'].split(' ')[0] for i in item)), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 阿含经词典
@get('/ccc/:page')
@view('temp/dict.jinja2')
def new_dict5(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with open('dict/ccc.json') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ' '.join(lookinkangxi(i)['pinyin'].split(' ')[0] for i in item)), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 威廉梵英词典
@get('/wm/:page')
@view('temp/dict.jinja2')
def new_dict6(page):
    q = request.GET.q
    pp = 800
    with gzip.open('dict/sa-en.json.gz') as fd:
        data = json.load(fd)

    header = data.pop('header', {})

    sa_en = HKdict2iast(data)

    if q:
        # 查字典
        fxcd = {item: re.split(r'\n *', sa_en[item])[1:] for item in sa_en}
        result = fxcd.get(q, {})
    else:
        # fxcd = [(item, re.split(r'\n *', sa_en[item])[1:]) for item in sa_en]
        # fxcd = [(item, sa_en[item]) for item in sa_en]
        fxcd = [((item, ''), sa_en[item]) for item in sa_en]
        total = len(fxcd)
        page = int(page)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# yates梵英词典
@get('/yates/:page')
@view('temp/dict.jinja2')
def new_dict6(page):
    q = request.GET.q
    pp = 800
    with gzip.open('dict/yat.json.gz') as fd:
        data = json.load(fd)

    header = data.pop('header', {})
    sa_en = HKdict2iast(data)

    if q:
        # 查字典
        fxcd = {item: re.split(r'\n *', sa_en[item])[1:] for item in sa_en}
        result = fxcd.get(q, {})
    else:
        # fxcd = [(item, sa_en[item]) for item in sa_en]
        fxcd = [((item, ''), sa_en[item]) for item in sa_en]
        total = len(fxcd)
        page = int(page)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}


# 15部巴利语英语词典
@get('/pali/:page')
@view('temp/dict.jinja2')
def new_dict7(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/pali-hant.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: data[item] for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, re.split(r'\n *', data[item])[1:]) for item in data]
        # fxcd = [(item, data[item]) for item in data]
        fxcd = [((item, ''), data[item]) for item in data]
        total = len(fxcd)
        page = int(page)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 巴利语汉语词典
@get('/pahant/:page')
@view('temp/dict.jinja2')
def new_dict8(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with open('dict/pali-dama.json') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 梵汉词典
@get('/sahant/:page')
@view('temp/dict.jinja2')
def new_dict8(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/sa-hant.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

#  阅藏知津
@get('/yzzj/:page')
@view('temp/dict.jinja2')
def new_dict9(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/yzzj.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

#  三藏法数
@get('/szfs/:page')
@view('temp/dict.jinja2')
def new_dict10(page):
    q = request.GET.q
    page = int(page)
    pp = 300
    with open('dict/szfsb.json') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        # fxcd = [((item, ''), (data[item]['def'], data[item].get('xr', ''))) for item in data]
        fxcd = [((item, ''), ('<br>'.join(data[item]), )) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

#  翻译名义集
@get('/fymyj/:page')
@view('temp/dict.jinja2')
def new_dict11(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with open('dict/fymyj.json') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

#  五灯会元
@get('/wdhy/:page')
@view('temp/dict.jinja2')
def new_dict12(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/wdhy.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

#  俗语佛源
@get('/syfy/:page')
@view('temp/dict.jinja2')
def new_dict12(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/syfy.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

#  于凌波
@get('/ylb/:page')
@view('temp/dict.jinja2')
def new_dict12(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with open('dict/ylb.json') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 历代名僧
@get('/ldms/:page')
@view('temp/dict.jinja2')
def new_dict12(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/ldms.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 百科全书
@get('/bkqs/:page')
@view('temp/dict.jinja2')
def new_dict12(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with gzip.open('dict/bkqs.json.gz') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        # fxcd = [(item, (data[item],)) for item in data]
        fxcd = [((item, ''), (data[item],)) for item in data]
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}

# 五译合璧
@get('/pentaglot/:page')
@view('temp/dict.jinja2')
def new_dict12(page):
    q = request.GET.q
    page = int(page)
    pp = 800
    with open('dict/pentaglot.json') as fd:
        data = json.load(fd)
    header = data.pop('header', {})
    if q:
        # 查字典
        fxcd = {item: (data[item],) for item in data}
        result = {(q, ''): fxcd.get(q, '没找到')}
        prevpage = max(page - 1, 1)
        nextpage = page + 1
    else:
        fxcd = []
        for item in data:
            content = []
            if 'san' in data[item]:
                content.append(f"梵語: {data[item]['san']}")
            if 'bod' in data[item]:
                content.append(f"泰語: {data[item]['bod']}")
            if 'mnc' in data[item]:
                content.append(f"满語: {data[item]['mnc']}")
            if 'mon' in data[item]:
                content.append(f"蒙語: {data[item]['mon']}")
            fxcd.append(((item, ''), content))
        total = len(fxcd)
        prevpage = max(page - 1, 1)
        nextpage = min(page + 1, total//pp+ 1 if total%pp> 0 else 0)
        result = dict(fxcd[pp*(page-1):pp*page])
    return {'result': result, 'header': header, 'prevpage': prevpage, 'nextpage': nextpage}


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


