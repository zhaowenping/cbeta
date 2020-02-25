import re
import os
from functools import total_ordering



def get_sorted_juan(book):
    '''获得book(T01)下的所有排序好的经卷号(T01n0002_001)'''
    # 对所有的book下的卷排序
    juanlist = []
    for path in os.listdir(f'xml/{book}'):
        sutra, vol = path[:-4].split('_')
        sutra = sutra.split('n')[1]
        juanlist.append((sutra, vol))
    juanlist.sort(key=lambda x: (int(f'{x[0]:0<5}', 16), int(x[1])))
    juanlist = [f'{book}n{i[0]}_{i[1]:0>3}' for i in juanlist]
    return juanlist

# lb anchor 0607a18  #p0481a25
# pb anchor T02.0125.0603c
@total_ordering
class Number:
    '''经号类: T01n0002a_002'''
    def __init__(self, n):
        self.book, self.tome, self.sutra, self.yiyi, self.volume = None, '', '', '', 0
        r = re.findall(r'([A-Z]{1,2})(\d{2,3})n(\w\d{3})([a-zA-Z])?(?:_(\d{3}))?', n)
        if r:
            self.book, tome, self.sutra, self.yiyi, self.volume = r[0]
            self.volume = 0 if not self.volume else int(self.volume)
            self.n = 2
            if self.book in {'A', 'C', 'G', 'GA', 'GB', 'L', 'M', 'P', 'U'}:
                self.n = 3
            tome = int(tome)
            self.tome = f'{tome:0{self.n}}'

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
        return (tt[self.book], int(self.tome), int(self.sutra, 16), yiyi, self.volume) < (tt[other.book], int(other.tome), int(other.sutra, 16), oyiyi, other.volume)

    def __str__(self):
        if not self.book:
            return 'None'
        if self.volume:
            return f'{self.book}{self.tome}n{self.sutra}{self.yiyi}_{self.volume:03}'
        else:
            return f'{self.book}{self.tome}n{self.sutra}{self.yiyi}'

    @property
    def url(self):
        if self.volume:
            return f'/xml/{self.book}{self.tome}/{self.book}{self.tome}n{self.sutra}{self.yiyi}_{self.volume:03}.xml'

    @property
    def url_with_anchor(self):
        if self.anchor:
            return f'/xml/{self.book}{self.tome}/{self.book}{self.tome}n{self.sutra}{self.yiyi}_{self.volume:03}.xml#{self.anchor}'
        if self.volume:
            return f'/xml/{self.book}{self.tome}/{self.book}{self.tome}n{self.sutra}{self.yiyi}_{self.volume:03}.xml'

    def get_first_juan(self):
        '''给定经号T01n0002，返回所有排序后的卷['001', '002', ...]中的第一个
        返回值是一个数字，如果没有找到则返回0'''
        number = f'{self.book}{self.tome}n{self.sutra}{self.yiyi}'
        # 查找第一卷(有些不是从第一卷开始的)
        juan = 999
        if not os.path.exists(f'xml/{self.book}{self.tome}'):
            return 0
        for path in os.listdir(f'xml/{self.book}{self.tome}'):
            if path.startswith(number):
                juan = min(juan, int(path.split('_')[1][:3]))
        if juan == 999:
            juan = 0
        return juan

    def get_next_juan(self, page):
        '''给定经号T01n0002_001，返回T01n0002_002'''
        # 重新生成标准经号
        if not self.volume:
            pass  #raise 一个错误?
        number = f'{self.book}{self.tome}n{self.sutra}{self.yiyi}_{self.volume:03}'
        # # 对所有的book下的卷排序
        juanlist = get_sorted_juan(f'{self.book}{self.tome}')
        idx = juanlist.index(number)
        if 0 <= idx + page < len(juanlist):
            return Number(juanlist[idx + page])
        # else: tome + 1
        # tomelist: 获得全部book(T01)下的所有排序好的册号列表(T01,T02,T03,T04...)
        page = page - (len(juanlist) - idx) + 1
        tomelist = (path.strip(self.book) for path in os.listdir(f'xml') if path.startswith(self.book))
        tomelist = tuple(f'{self.book}{i}' for i in sorted(tomelist, key=int))
        idx = tomelist.index(f'{self.book}{self.tome}')
        print(idx, page, len(tomelist))
        # page<0 and 0 <= idx - 1 , page >0  and
        if idx + 1 < len(tomelist):
            nextbook = tomelist[idx + 1]
            juanlist = get_sorted_juan(nextbook)
            return Number(juanlist[page-1])
        # else: book + 1
        return juanlist

    def get_prev_juan(self):
        '''给定经号T01n0002_002，返回T01n0002_001'''
        # 重新生成标准经号
        if not self.volume:
            pass  #raise 一个错误?
        number = f'{self.book}{self.tome}n{self.sutra}{self.yiyi}_{self.volume:03}'
        # 对所有的book下的卷排序
        juanlist = get_sorted_juan(f'{self.book}{self.tome}')

        if number != juanlist[0]:
            return Number(juanlist[juanlist.index(number) - 1])
        # else: book - 1
        # 获得全部排序号的book列表
        booklist = (path.strip(self.book) for path in os.listdir(f'xml') if path.startswith(self.book))
        booklist = sorted(booklist, key=int)
        booklist = [f'{self.book}{i}' for i in booklist]
        # if book != booklist[0]:
        if f'{self.book}{self.tome}' != booklist[0]:
            prevbook = booklist[booklist.index(book) - 1]
            booklist = get_sorted_juan(prevbook)
            return Number(booklist[-1])
        # else:
        return juanlist


    def get_next_juan2(self, page):
        '''给定经号T01n0002_001，返回T01n0002_002'''
        # 重新生成标准经号
        if not self.volume:
            pass  #raise 一个错误?
        number = f'{self.book}{self.tome}n{self.sutra}{self.yiyi}_{self.volume:03}'
        # # 对所有的book下的卷排序
        juanlist = get_sorted_juan(f'{self.book}{self.tome}')
        idx = juanlist.index(number)
        if 0 <= idx + page < len(juanlist):
            return Number(juanlist[idx + page])
        # else: tome + 1
        # page = page - (len(juanlist) - idx) + 1
        page = - page - idx
        print(idx, page)
        tomelist = (path.strip(self.book) for path in os.listdir(f'xml') if path.startswith(self.book))
        tomelist = [f'{self.book}{i}' for i in sorted(tomelist, key=int)]
        idx = tomelist.index(f'{self.book}{self.tome}')
        #print(idx, page, len(tomelist))
        # page<0 and 0 <= idx - 1 , page >0  and
        if idx + 1 < len(tomelist):
            nextbook = tomelist[idx - 1]
            juanlist = get_sorted_juan(nextbook)
            return Number(juanlist[-page])
        # else: book + 1
        return juanlist


title1 = 'T07n0007_001'
title2 = 'T07n0007_002'
# n = Number(title1)
# print(title, str(n), Number(title1)< Number(title2))
# n = Number('T01n0026')
# print(n.get_all_juan())

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




# import os
# r = set()
# for path in os.listdir(f'../xml'):
#     r.add(re.sub(r'[0-9]*', '', path))
# J32nB271
title = 'LC07n0007_001'
title = 'ZW02n0018a_001'
title = 'T01n0098_001'
title = 'T02n0099_001'

n = Number(title)
print(n)
#print(n.get_next_juan(-1), n.get_prev_juan(), n, n.get_next_juan(1), n.get_next_juan(2))
#print(n.get_next_juan(-1), n.get_next_juan(1), n.get_next_juan(2))
print(n.get_next_juan2(-1).url, n.url)
#print(n.get_next_juan(10))
