import re
import os
from functools import total_ordering

title = 'LC07n0007_001'
title = 'ZW02n0018a_001'

# J32nB271

@total_ordering
class Number:
    '''经号类: T01n0002a_002'''
    def __init__(self, n):
        self.book, self.tome, self.sutra, self.yiyi, self.volume = None, 0, 0, '', 0
        r = re.findall(r'([A-Z]{1,2})(\d{2,3})n(\w\d{3})([a-zA-Z])?(?:_(\d{3}))?', n)
        if r:
            self.book, self.tome, self.sutra, self.yiyi, self.volume = r[0]
            self.tome = int(self.tome)
            self.sutra = int(self.sutra, 16)
            self.volume = 0 if not self.volume else int(self.volume)
            self.n = 2
            if self.book in {'A', 'C', 'G', 'GA', 'GB', 'L', 'M', 'P', 'U'}:
                self.n = 3
            self.tome = f'{self.tome:0{self.n}}'

    def __eq__(self, other):
        return (self.book == other.book and
                self.tome == other.tome and
                self.sutra == other.sutra and
                self.yiyi == other.yiyi and
                self.volume == other.volume)

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
        return (tt[self.book], int(self.tome), self.sutra, yiyi, self.volume) < (tt[other.book], int(other.tome), other.sutra, oyiyi, other.volume)

    def __str__(self):
        if not self.book:
            return 'None'
        if self.volume:
            return f'{self.book}{self.tome:0{self.n}}n{self.sutra:04}{self.yiyi}_{self.volume:03}'
        else:
            return f'{self.book}{self.tome:0{self.n}}n{self.sutra:04}{self.yiyi}'

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



import os
r = set()
for path in os.listdir(f'../xml'):
    r.add(re.sub(r'[0-9]*', '', path))

print(r)
