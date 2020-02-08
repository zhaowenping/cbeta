import pprint
import re
from functools import reduce
import json

def pagerank(filename, sentence='', content=''):
    '''对xml文件名评分, filename 为 T20n1060 或者 T20n1060_001.xml 形式
    A,B,C,D,F,G,GA,GB,I,J,K,L,M,N,P,S,T,U,X,ZW, Y, LC
    '''
    # sentence = sentence.strip().split()
    # sentence_value = sum([{True:0, False:1}[s in content] for s in sentence])
    pr = ("T", "B", "ZW", "A", "C", "D", "F", "G" , "GA", "GB", "I", "J", "K", "L", "M", "N", "P", "S", "U", "X", "Y", "LC")
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

def rm_variant(x):
    return x

def read_menu_file(sutra_list):
    '''读取tab分隔的菜单文件，返回树状字典'''
    menu = dict()
    print('''读取tab分隔的菜单文件，返回树状字典''')

    with open(sutra_list, encoding='utf8') as fd:
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

class Search:
    def __init__(self, norm=True):
        # mulu = read_menu_file("static/sutra_sch.lst")
        # #pprint.pprint(m['T 大正藏'])
        # # d = mulu['T 大正藏']
        # def walk(d, result=[]):
        #     '''遍历目录树'''
        #     for x in d:
        #         if not d[x]:
        #             result.append(x)
        #         else:
        #             walk(d[x], result)
        #     return result


        # result = walk(mulu)
        # result = [i.split(maxsplit=2) for i in result]

        # pprint.pprint(result)
        # if norm:
        #     titles = [(i[0], ' '.join((rm_variant(i[1]), i[2]))) for i in result]
        # else:
        #     titles = [(i[0], ' '.join((i[1], i[2]))) for i in result]
        # pprint.pprint(titles)
        # pprint.pprint(titles)
        titles = []
        with open("static/sutra_sch.lst") as fd:
            for line in fd:
                if 'n' in line:
                    line = line.strip().split(maxsplit=1)
                    titles.append(line)

        # titles 是经号和title的对照表
        # 生成索引表
        self.index = {}
        for i in titles:
            z = 0
            #print(i)
            for j in i[1]:
                if j in self.index:
                    self.index[j].append((i[0], z))
                else:
                    self.index[j] = [(i[0], z),]
                #print(j, i[0], z)
                z += 1
        for i in self.index:
            # print(i)
            v = self.index[i]
            r = dict()
            for j in v:
                if j[0] in r:
                    r[j[0]].append(j[1])
                else:
                    r[j[0]] = [j[1],]
            # pprint.pprint((i, r))
            self.index.update({i: r})
        self.titles = dict(titles)
        #pprint.pprint(self.index)
        # print(json.dumps(self.index))

    def search(self, title, norm=True):
        if norm:
            title = rm_variant(title)
        result = (set(self.index.get(tt, {}).keys()) for tt in list(title))
        return sorted(reduce(lambda x, y: x & y, result), key=pagerank)

ss = Search()
print(ss.search('中靖國續'))

# 372     for idx in ss.search(title):
# 373         title0 = idx
# 374         hl = ss.titles[idx]
# 375         zang = idx.split('n')[0]              # T01
# 376         juan = get_all_juan(idx)[0]           # 001
# 377         an = f"/xml/{zang}/{idx}_{juan}.xml"  # T01n0002_001.xml
# 378         results.append({'hl': hl, 'an':an, 'title':title0, 'author':''})


