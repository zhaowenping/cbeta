#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2018-01-18 15:25:27
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

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *
import psycopg2
# import opencc

import pprint
from libhan import hk2sa, read_menu_file
from libhan import get_all_juan
from libhan import Search
from libhan import TSDetect
from libhan import convert2t
from libhan import convert2s
from libhan import normyitizi
from libhan import fullsearch

from libhan import lookup, lookinkangxi, lookinsa
from libhan import unihan

# from xsltproc import xsltproc, XSLT

# XSLT_FILE = 'static/tei.xsl'

@route('/')
@view('temp/index.html')
def index():
    return {'Hello World!':''}

@route('/tools')
@view('temp/tools.html')
def tools():
    return {'Hello World!':''}

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
sch_c = "static/long.lst"

@route('/mulu')
@view('temp/menu.jinja2')
def menu():
    menu = read_menu_file(sch_b)
    return {'menus': menu, 'request':request, 'yiju': '大正藏部類'}

@route('/qianlong')
@view('temp/menu.jinja2')
def menu():
    menu = read_menu_file(sch_c)
    return {'menus': menu, 'request':request, 'yiju': '乾隆藏'}

@route('/cebie')
@view('temp/menu.jinja2')
def menu():
    menu = read_menu_file(sch_a)
    return {'menus': menu, 'request':request, 'yiju': '大正藏冊別'}

@route('/mulu/:bulei#.+#')
@view('temp/menu.jinja2')
def submenu(bulei):
    menu = read_menu_file(sch_b)
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
def submenu(bulei):
    menu = read_menu_file(sch_a)
    #pprint.pprint(menu)
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
        # 查找第一卷(有些不是从第一卷开始的)
        juan = get_all_juan(sutra)[0]           # 001
        url = f"/xml/{zang}/{sutra}_{juan}.xml"  # T01n0002_001.xml
        redirect(url)
    return {'menus': menu, 'request':request, 'nav':nav, 'yiju': '大正藏冊別', 'root': root}


# 处理搜索

ss = Search()
ts = TSDetect()

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
        title = re.sub(r'[一二三四五六七八九十]+卷', '', title)
    else:
        title = request.forms.content
    if ts.detect(title)['confidence'] == 's':
        # title = opencc.convert(title, config='s2t.json')
        title = convert2t(title)
    results = []
    for idx in ss.search(title):
        title0 = idx
        hl = ss.titles[idx]
        zang = idx.split('n')[0]              # T01
        juan = get_all_juan(idx)[0]           # 001
        an = f"/xml/{zang}/{idx}_{juan}.xml"  # T01n0002_001.xml
        results.append({'hl': hl, 'an':an, 'title':title0, 'author':''})
    if request.method == "GET":
        # 0个结果页面不动,多个结果自己选择
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
    print('发过来一个字:%s' % word)
    pinyin = ''
    _from = ''
    definition = ''
    if len(word) == 1:
        result = lookinkangxi(word)
        _from = result['from']
        definition = result['def']
        pinyin = result['pinyin']
    else:
        rr = lookup(word)
        _from = rr['from']
        definition = rr['definition']

    if not _from:
        result = lookinsa(word)
        _from = result['from']
        definition = result['def']
        pinyin = result['pinyin']

    # if not _from:
    #     definition = sa_hant.get(hk2sa(word).lower(), '')
    #     if definition:
    #         _from = "文理学院"
    #         pinyin = "文理学院"
    # if not definition:
    #     # 使用Harvard-Kyoto转写查找字典
    #     definition = sa_en.get(hk2sa(word), '')
    #     # 使用缩写查找字典
    #     if not definition:
    #         w = word.replace('1', '').replace("'", '').replace('4', '').replace('7', '').replace('8', '').replace('9', '').replace('0', '').replace('-', '').lower()
    #         definition = sa_en.get(w, '')
    #     if definition:
    #         definition = '|'.join(definition)
    #         _from = "威廉梵英词典"
    #         pinyin = "威廉梵英词典"
    # if not definition:
    #     print(hk2sa(word))
    #     definition = yat.get(hk2sa(word), '')
    #     if not definition:
    #         w = word.replace('-', '').lower()
    #         definition = yat.get(w, '')
    #     if definition:
    #         definition = '|'.join(definition)
    #         _from = "YAT"
    #         pinyin = "YAT"

    # 用Unicode数据库注音
    if _from and not pinyin:
        pinyin = ' '.join([unihan.get(x, {}).get('kMandarin', '').split()[0] for x in word])
    # print(pinyin, definition)

    # else:
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
    with open(filename) as fd:
        content = fd.read()
    content = content.replace("<TEI ", "<TEI xml:lang='lzh-Hans' ")
    # 简体繁体双引号, 单引号切换
    content = content.translate({0x300c: 0x201c, 0x300d: 0x201d, 0x300e: 0x2018, 0x300f: 0x2019})
    response.content_type = 'text/xml'
    # content = opencc.convert(content, config='t2s.json')
    content = convert2s(content)
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

@get('/diff')
@view('temp/diff.jinja2')
def diff_get():
    return {}

import difflib
from difflib import *
import chardet
import jieba
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
    print(request.forms.punct)
    print(request.forms.punct == 'true')
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


    # lfile.save('lfile.tmp', overwrite=True)
    # rfile.save('rfile.tmp', overwrite=True)
    # from subprocess import Popen, PIPE
    # p2 = Popen(["diff", "lfile.tmp", "rfile.tmp"], stdin=PIPE, stdout=PIPE)
    # output = p2.communicate()[0]
    # output = output.decode('utf8')

    # ll = output.splitlines()[1::4]
    # rr = output.splitlines()[3::4]
    # lfile = open('lfile.tmp').read()
    # rfile = open('rfile.tmp').read()
    # print(''.join(list(difflib.Differ().compare(lfile, rfile))))

    d = Differ()
    with open('lfile.tmp') as fd:
        lfile = fd.read()
        # lfiles = [line.strip() for line in lfile.splitlines()]

    with open('rfile.tmp') as fd:
        rfile = fd.read()
        # rfiles = [line.strip() for line in rfile.splitlines()]

    # result = list(d.compare(lfiles, rfiles))
    result = list(d.compare(lfile, rfile))

    lfile = []
    rfile = []
    for line in result:
        if line.startswith(' '):
            line = line[2:]
            lfile.append(f'<span class="orig">{line}</span>')
            rfile.append(f'<span class="orig">{line}</span>')
        elif line.startswith('- '):
            line = line[2:]
            lfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('+ '):
            line = line[2:]
            rfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('?'):
            continue
    lfile = ''.join(lfile)
    rfile = ''.join(rfile)

    return {'lfile': lfile, 'rfile': rfile}

# jieba.load_userdict('dict/terms.txt')
@get('/diff/word')
@view('temp/diff.jinja2')
def diff_word_get():
    '''按照词比较两个文件不同'''
    d = Differ()
    with open('lfile.tmp') as fd:
        lfile = fd.read()
        lfile = list(jieba.cut(lfile))
        # lfiles = [line.strip() for line in lfile.splitlines()]

    with open('rfile.tmp') as fd:
        rfile = fd.read()
        rfile = list(jieba.cut(rfile))
        # rfiles = [line.strip() for line in rfile.splitlines()]

    # result = list(d.compare(lfiles, rfiles))
    result = list(d.compare(lfile, rfile))

    lfile = []
    rfile = []
    for line in result:
        if line.startswith(' '):
            line = line[2:]
            lfile.append(f'<span class="orig">{line}</span>')
            rfile.append(f'<span class="orig">{line}</span>')
        elif line.startswith('- '):
            line = line[2:]
            lfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('+ '):
            line = line[2:]
            rfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('?'):
            continue
    lfile = ''.join(lfile)
    rfile = ''.join(rfile)

    return {'lfile': lfile, 'rfile': rfile}

@get('/diff/line')
@view('temp/diff.jinja2')
def diff_line_get():
    '''按照行比较两个文件不同'''
    d = Differ()
    with open('lfile.tmp') as fd:
        lfile = fd.read()
        lfiles = [line.strip() for line in lfile.splitlines()]

    with open('rfile.tmp') as fd:
        rfile = fd.read()
        rfiles = [line.strip() for line in rfile.splitlines()]

    result = list(d.compare(lfiles, rfiles))
    # result = list(d.compare(lfile, rfile))

    lfile = []
    rfile = []
    for line in result:
        if line.startswith(' '):
            line = line[2:]
            lfile.append(f'<span class="orig">{line}</span>')
            rfile.append(f'<span class="orig">{line}</span>')
        elif line.startswith('- '):
            line = line[2:]
            lfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('+ '):
            line = line[2:]
            rfile.append(f'<span class="red">{line}</span>')
        elif line.startswith('?'):
            continue
    lfile = ''.join(lfile)
    rfile = ''.join(rfile)

    return {'lfile': lfile, 'rfile': rfile}


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


