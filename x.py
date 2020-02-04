import re
import os
from functools import total_ordering

title = 'LC07n0007_001'
title = 'ZW02n0018a_001'


@total_ordering
class Number:
    '''经号类: T01n0002a_002'''
    def __init__(self, n):
        self.book, self.ce, self.sutra, self.yiyi, self.juan = None, 0, 0, '', 0
        r = re.findall(r'([A-Z]{1,2})(\d{2,3})n(\d{4})([a-hA-F])?(?:_(\d{3}))?', n)
        if r:
            self.book, self.ce, self.sutra, self.yiyi, self.juan = r[0]
            self.ce = int(self.ce)
            self.sutra = int(self.sutra)
            self.juan = 0 if not self.juan else int(self.juan)

    def __eq__(self, other):
        return (self.book == other.book and
                self.ce == other.ce and
                self.sutra == other.sutra and
                self.yiyi == other.yiyi and
                self.juan == other.juan)

    def __lt__(self, other):
        '''重要性的排序'''
        pr = ("T", "A", "S", "F", "C", "K", "B", "ZW", "P", "U", "D", "G", "M", "N", "L", "J", "X", "Y", "LC", "GA", "GB", "I")
        tt = {  'T': 1, 'A': 2, 'F': 3, 'S': 4, 'U': 5,
                'P': 6, 'B': 7, 'ZW': 8, 'J': 9, 'C': 10,
                'D': 11, 'K': 12, 'G': 13, 'N': 18, 'I':19,
                'L': 20, 'M': 30, 'Y':40, 'LC':50,
                'GA':60, 'GB': 70, 'ZS':80, 'X':90}
        yiyi = 0 if not self.yiyi else int(self.yiyi, 16)
        oyiyi = 0 if not other.yiyi else int(other.yiyi, 16)
        return (tt[self.book], int(self.ce), self.sutra, yiyi, self.juan) < (tt[other.book], int(other.ce), other.sutra, oyiyi, other.juan)

    def __str__(self):
        if not self.book:
            return 'None'
        n = 2
        if self.book in {'A', 'C', 'G', 'GA', 'GB', 'L', 'M', 'P', 'U'}:
            n = 3
        if self.juan:
            return f'{self.book}{self.ce:0{n}}n{self.sutra:04}{self.yiyi}_{self.juan:03}'
        else:
            return f'{self.book}{self.ce:0{n}}n{self.sutra:04}{self.yiyi}'

    def get_all_juan(self):
        '''给定经号T01n0002，返回所有排序后的卷['001', '002', ...]
        返回值是一个数组，如果没有找到则返回空的数组'''
        book, sutra = str(self).split('n')
        number = str(self).split('_')[0]
        # 查找第一卷(有些不是从第一卷开始的)
        juan = []
        if not os.path.exists(f'xml/{book}'):
            return None
        for path in os.listdir(f'xml/{book}'):
            if path.startswith(number):
                juan.append(path.split('_')[1][:-4])
        juan.sort(key=lambda x: int(re.sub(r'[a-zA-Z]*', '', f'{x:0<5}'), 16))
        return juan

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



title1 = 'T07n0007_001'
title2 = 'T07n0007_002'
n = Number(title)
print(title, str(n), Number(title1)< Number(title2))
n = Number('T01n0026')
print(n.get_all_juan())

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


import os
r = set()
for path in os.listdir(f'../xml'):
    r.add(re.sub(r'[0-9]*', '', path))

print(r)
