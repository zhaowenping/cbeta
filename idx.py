#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Language Version: 2.7+
# Last Modified: 2023-04-06 16:32:40
from __future__ import unicode_literals, division, absolute_import, print_function

"""

"""

__all__ = []
__author__ = "北京秘银科技 赵文平(email:wenping_zhao@126.com tel:13511028685)"
__version__ = "0.0.1"


bs = dict()
bushou = set()
with open('idx/ids.txt') as fd:
    for line in fd:
        line = set(line.split()[2])
        for e in line:
            bushou.add(e)
            if e not in bs:
                bs[e] = 1
            else:
                bs[e] += 1
        #print(line)

kangxi = ''' 一 丨 丶 丿 乙 亅
二 亠 人 儿 入 八 冂 冖 冫 几 凵 刀 力 勹 匕 匚 匸 十 卜 卩 厂 厶 又
口 囗 土 士 夂 夊 夕 大 女 子 宀 寸 小 尢 尸 屮 山 巛 工 己 巾 干 幺 广 廴 廾 弋 弓 彐 彡 彳
心 戈 戶 手 支 攴 文 斗 斤 方 无 日 曰 月 木 欠 止 歹 殳 毋 比 毛 氏 气 水 火 爪 父 爻 爿 片 牙 牛 犬
玄 玉 瓜 瓦 甘 生 用 田 疋 疒 癶 白 皮 皿 目 矛 矢 石 示 禸 禾 穴 立
竹 米 糸 缶 网 羊 羽 老 而 耒 耳 聿 肉 臣 自 至 臼 舌 舛 舟 艮 色 艸 虍 虫 血 行 衣 襾
見 角 言 谷 豆 豕 豸 貝 赤 走 足 身 車 辛 辰 辵 邑 酉 釆 里
金 長 門 阜 隶 隹 雨 靑 非
面 革 韋 韭 音 頁 風 飛 食 首 香
馬 骨 高 髟 鬥 鬯 鬲 鬼
魚 鳥 鹵 鹿 麥 麻
黃 黍 黑 黹
黽 鼎 鼓 鼠
鼻 齊
齒
龍 龜
龠
'''.split()

kangxi = '''乚  𠃊 𠃑 ⺄ 丨 丶 丿 亅 𠃍 𠄎
 2 ⺇𠘨 ⺈ 丆 阝 亻 㔾 刂 𠂉 𠆢 㐅 丷 コ 𠂆 亠 冂 冖 冫 凵 勹 匚 匸 卩 厶 丂 𠃎 ⺊ 𠤎
 3 艹 犭 辶 ⻎ ⻍ 氵 扌 忄 𰀁 夨 䒑 丬 卪 囗 夂 宀 尢 屮 巛 幺 廴 廾 弋 𠂋 彐 彡 彳 乆 㐄 𭕄 𱍸
 4 爫 灬 ⺼ 𱼀 𧘇 𠔿 𦉪 龷 龶 龰 ⺗ 戶 毋 爿 朩 攵 𰀡
 5 衤 罒 𡗜 氺 𡗗 𰀉 𠀐 𠂕 𤴓 疋 疒 癶 ⺪
 6 𠔉 龹 𭤨 覀 襾 𠂢 𥫗 𠇍 糸 耒 聿 舛 艮 艸 虍
 7 𢦏 镸 𠂭 𦣻 見 豕 豸 貝 車 辵 邑 釆 攸
 8 飠 𠦝 𨸏 長 門 阜 隹 靑 𠧢
 9 𩙿 韋 頁 風 飛
10 𭆆 𰮤 𤇾 𣪊 𡨄 馬 髟 鬥 鬯 鬲
11 𠩺 𦰩 𠁳 魚 鳥 鹵 麥
12 𤔔 黃 黍 黹 黽
13 𦥯 𣪠 𣎆
14 𰯲 齊
15 𢀩 齒
16 𩰲 龍 龜
17 龠
19 䜌
𤰇 𠀗
'''.split()

import pprint
import pprint
print(kangxi)
for e in kangxi:
    if e in bushou:
        bushou.remove(e)

#for e in bushou:
#    if e not in kangxi:
for e in kangxi:
    if len(e) !=1: continue
    print(e, 'U+%X' % ord(e), bs.get(e, None))
print(len(bushou))
#pprint.pprint(bs)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    # main()
    test()

