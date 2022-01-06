# 大藏经开源阅读计划  (做最好的开源阅藏程序)

因为cbeta是用C++写的，我这里没有正版windows，所以一直是把cbeta光盘中的xml拷贝下来，自己处理之后阅读。
最近cbeta的xml格式发生了变化(从TEI.2格式转为P5格式)。所以重写了我的程序。随便共享出来给有需要的人。
随便加了巴利文、梵文、藏文、英文、日文佛经，同时加以汉语正字法和异文逐段对读功能，以期获得准确理解

## 主要特点

1. 舒适的阅读体验！主要针对Linux与苹果优化. (Windows暂时显示效果不佳)
   1. 对市面上流行的大约40多款字体进行了测试。选择最适合电子设备阅读的字体。主字体采取冬青黑字体
   2. 对适合长时间阅读的护眼模式进行了深入研究和测试
   3. 完全的去除了各种组合字，可以在线显示，不需要安装字体
   4. 美化标点的显示效果。使之自然美观
2. 完全符合UNICODE国际标准。不使用geek技术来处理文本。这意味着即使txt文档，也有良好的显示效果和排版。
   1. 梵文悉曇体完全使用unicode13.0标准显示, 搜索; 对悉昙字母标注了罗马注音
   2. 梵文兰扎体完全使用unicode13.0草案标准显示, 搜索; 对兰扎字母标注了罗马注音
   3. 生僻字使用到H区汉字
3. 首次提出佛经阅读，需要区分版本为原版和正字版，原版尽力显示原貌；正字版提供正字法方便快速、准确的阅读。简体版建立在正字版基础之上，对有歧义的繁体字不做转换
4. 原字版本
   1. 目标为在国际标准前提下对藏经原貌的完全还原
   2. 补全cbeta缺失的数万生僻字。 
   3. 恢复异体字在藏经中的原貌, 使用藏经中原有字形显示
5. 正字法版本
   1. 目标争取做到一字一音一义。也就是一个字只有一个发音，一个含义。见字立刻知道发音，知道含义。所以可以实现对佛经的极速阅读。
   2. 完全去除异体字和通假字。方便快速、无歧义阅读和搜索。
   3. 设备一致性：去除了中日韩兼容字符区（F900 ~ FAFF）的汉字，只保留了常规汉字(﨎﨏﨑﨓﨔﨟﨡﨤﨧﨨﨩)11个字; 去除了兼容汉字区的汉字,只保留了(你 U+2F804)一个字(未来使用ivd方式去除)，吆(U+2F83B)字替换为䶸(U+4DB8)，﨣 U+FA23替换为𧺯 U-00027EAF
   4. 异体字和通假字的规范化(基本按照康熙字典标准，次之使用台湾教育部字典, 次之依照大陆简化字和藏经高频取为标准字)
   5. 使用更多的分化字表达不同的含义，避免极速阅读时的歧义：例如校与挍分化为名词与动词，滾只保留水貌的含义。
   6. 繁体字广、胜、义、叶、坏分别对应简体字为（摩、魔..)、腥、叉、协、坯
   7. 对大量可文本化的图片文本化。尽量去除无用图片
6. 校勘、集成多部（目前为止大约40多部）权威性字典词典，更方便的查询词典/字典
7. 各种极为方便的快捷方式，使得可以直接搜索到想要的内容、标题、作者
8. 对计算机友好的完全开放的接口, url支持命令行操作, 支持多种输出形式:xml, json, pdf, html, epub, docx, mp3...
9. 拼音标注, 语音合成，自动朗读, 盲人模式
10. 对大藏经作适量的插图，减轻长时间阅读的疲劳感。加深各种境界的理解。将图片全部修改为SVG高清格式


## 目标
1. 标准。完全使用符合国际标准的技术来实现。诸如unicode14.0,html5... 可以在几乎任何操作系统、浏览器上获得完全一致的体验。
2. 专业。尽力还原古籍原貌，不做妥协。
3. 易用。对非专业人士和障碍人士友好。不要求你必须懂文献文、校勘学、版本学等各种学问，也不要求你必须懂繁体字、梵巴藏英文，不要求你必须识字，也不要求你必须有良好的视觉、听觉。
4. 清净。整个项目的全部内容都没有使用任何私有或者可能存在版权争议的资源，除了兼容性测试。也不接受有限制条款的基金支持。例如(文字、图像、代码)编辑器、私有的编程语言（例如VC++、java等)、数据库（例如mysql)、操作系统(例如windows)。

## 版权
1. 禁止。任何导致作者有可能不能使用自己的资源的行为都是禁止的。我在任何情况下都完全拥有使用自己代码、资源的权力，所有权、著作权，修改权，无论你怎么修改这些资源。
2. 继承。任何使用此项目私有资源、代码片段的项目，都将自动转为开源项目，否则都属于盗版。
免责声明：因为免费所以免责。如果(因为使用此软件)出了什么事情，都是你自己的事儿，CPU过热烧毁，和老婆吵架了，或者破坏了世界和平，毁灭了宇宙，都跟我一点关系都没有，不要来找我！本人不保障此软件的安全性，不保障软件中没有包含病毒、蠕虫或者其他任何有害程序。 
3. 因为这是自由软件，但是不是免费软件，所以此资源完全可以通过商业途径传播，可以倒找钱、白送、高价、天价或者宇宙价出售光盘/U盘/硬盘, 可以随有价光盘/U盘一起赠送！这些不需要本人的任何授权！也不需要通知本人。

## 与cbeta阅读器的差异
1. 快如闪电! 稳如磐石!
2. 全面支持unicode 13.0. 使用unicode显示悉昙和兰扎梵文. 使用: https://en.wikipedia.org/wiki/Siddha%E1%B9%83_script
3. 使用最新版本的unicode显示异体字，尽可能的使用接近藏经原貌的字; 不使用兼容字。(包括A、B、C、D、E、F、G、H、I区汉字)
4. 支持简体阅读和简体搜索, 支持转换异体字为正字
5. 集成多部字典词典，划词查询, 方便易用; 使用Levenshtein算法查询词典
6. 标点符号破折号替换为单一字符，不会断开。
7. 使用python和xslt编写，可以运行在目前几乎所有主流操作系统中: 从meego到AIX。
8. cbeta在注释问题字段的时候使用两个anchor标签夹在一起的做法。导致获得这些字段非常困难, 考虑替换成orig标签，以便自由切换不同藏经
9. 无上士调御丈夫 中间的标点去掉
10. 校勘了大约数1000万处原文错误的字词，相比cbeta校对约1000万处(数量是大概统计)


## 技术方式和预期效果

1. 速度.目前来看相比CBETA速度快上很多。完全不消耗服务器资源。对浏览器的消耗也非常小。速度非常快。CBETA在多处有卡顿的现象。原因不明，阅读体验不佳
目前唯一发现有些微卡顿的是' 胎藏梵字真言上卷', (T18/T18n0854_001.xml),用时0.5秒降为0.09秒，原因是使用了太多的图片和文件比较大所导致;优化速度后最大(2.7M)的文件'朝鮮佛教通史'(B31n0170_003.xml)由0.9秒降低为0.45秒，
原来速度最慢的K35n1257_025由2.5秒降为0.25秒,已经可用
2. 代码非常少。修改部署容易
4. 自制的悉昙字字体已经正常, 使用Unicode10.0的码表来显现, ttf文件只有9k大小
5. 部分Ｆ区汉字使用了webfont技术，不需要安装字库即可正常显示(没有覆盖全部用到的Ｆ区汉字, 所以还是需要安装大字库)
6. 整体程序非常简单。只有一个tei.xsl文件和一个tei.css文件作为显示效果。而阅读效果比较好。修改简单方便，适合长期阅读藏经使用。


## 技术方式

1. 使用xslt来处理xml, 然后使用在xml中直接嵌入xslt的方式, 就可以直接在浏览器中阅读了。
如果希望自己使用的人, 可以自己搭建一个nginx服务器。将静态文件指向xml和tei.xsl,tei.css文件所在目录即可; 甚至只需要把xml文件, tei.xsl和tei.css文件放在一起即可使用

2. 使用python来处理其他事情, 主要是生成目录, 搜索

3. 尽量少的使用js控制， 尽量少的使用数据库, 前端生成内容, 对搜索引擎友好, 对爬虫友好

4. 在线直接阅读xml文件. 不单独生成html，占用空间小。 pdf格式文件使用xsl-fo方式直接在线生成


## 安装说明

1. 示例是在ubuntu16.04上所做。其他操作系统仿照即可。不需要安装数据库，web服务器，只需要安装python即可
2. 假设安装到$HOME/cbeta目录
3. 安装python虚拟环境, 会生成一个py36的目录，里面是python的可执行程序(需要python3.6及以上版本)
```
 $ git clone https://github.com/zhaowenping/cbeta.git
 $ cd cbeta
 $ python3 -m venv py36
 $ cd py36
 $ . bin/activate
 $ cd ..
 $ pip install --upgrade pip
 $ pip install -r requirements.txt
 ```
4. 将全部的xml文件移动到 cbeta/xml目录中,原有目录保留, 需要使用make_xml.py文件生成, 主要作用是两个，第一，去掉xml文件中的默认地址空间，第二，添加tei.xsl文件的链接上去
5. 运行程序 $ python reader.py
6. 打开浏览器，默认地址 http://localhost:8081 即可看到

## 使用说明

1. 系统支持部分restful接口。
2. 在阅读中查询某字或者某词，使用鼠标选中希望查询的字词，然后把鼠标悬浮到被选择的字词上，如果在字典中存在被查询的字词，就会自动悬浮显示
3. 单独使用字典词典，例如查询'仁'字, 可以在浏览器中输入 http://localhost:8081/dict/仁
4. 查詢指定字典词典，例如在丁福保詞典中查询'佛陀'一詞, 可以在浏览器中输入 http://localhost:8081/dict/dfb/佛陀 , 目前可以查詢的有fk,kangxi,ccc,fxcd,dfb
5. 支持dict协议(rfc2229), 使用 $ apt install dict 安装dict客户端。使用$ dict 佛陀 -h kepan.org 即可查询字典

## 文件列表
1. static/tei.xsl 主体程序
2. static/taisho.xsl 大正藏转换程序
3. static/siddham.ttf 符合unicode10.0的悉昙体字库
4. static/siddham.sfd 符合unicode10.0的悉昙体字库的fontforg文件，可以根据这个文件继续修改字库
5. static/siddham.woff 符合unicode10.0的悉昙体字库,可以通过webfont方式使用悉昙体字库，以便读者不用安装字库即可阅读悉昙体
6. terms.txt  佛教词汇大全，目前搜集了不到8万词汇，用来给藏经分词用的, 以便全文检索使用
7. w_normal.txt 制作的组合字表, 用来清洗xml文档
8. yoga 目录,打算后期为瑜伽师地论做现代化标点
9. reader.py python的web程序入口, 提供目录、搜索等服务
10.  .lst文件 tab分割的目录文件
11. temp目录, 页面的jinja2模板文件
12. fo目录, 使用fop程序生成pdf的程序，使用的时候需要修改fop.xconf文件中的directory标签，指向字库文件目录(fop2.1)
13. cb-Siddam.woff 原cbeta的悉檀字庫，因爲不標準所以轉換而成
14. dictd.py 文件: 支持[dict协议](https://tools.ietf.org/html/rfc2229) 的字典查询服务器程序


## 字库

1. 页面整体上是使用冬青黑体或者苹方字体显示主要文字，使用SimSun显示标点符号，你可以随意修改为自己喜欢的字体
2. 建议下载花園明朝(HanaMin)字体以便显示生僻字  http://fonts.jp/hanazono/ 或者 http://ctext.org/font-test-page/zh, 因为花园字体是自由字体，尤其是花園明朝B一定要安装
3. 安装天城体字体命令: sudo apt install fonts-deva

## 词典

在转码过程中的错误使用U+FFFD替换，需要进一步的校对原文；法相词典下都需要进一步校堪工作

|序号| 词典                           | 文件名                       |  词条数量|  注释      | 
|----| -------------------------------|:----------------------------:| --------:|----------- | 
| 1. | 庄春江汉译阿含经词典ver4       | ccc.json                     |   4573   |            |
| 2. | 佛學常見詞彙（陳義孝）         | cxy.json                     |   5858   |            |
| 3. | 丁福保《佛學大辭典》           | dfb.json.gz                  |  31366   |            |
| 4. | 佛光大辞典                     | fk.json.gz                   |  24445   |            |
| 5. | 康熙字典                       | kangxi.json.gz               |  26341   |            |
| 6. | 《南山律學辭典》               | nvd.json                     |   6025   |            |
| 7. | 威廉梵英词典                   | sa-en.json.gz                | 160625   |            |
| 8. | 15部巴利语词典                 | pali-hant.json.gz            |  49111   |            |
| 9. | 三藏法数                       | szfs.json                    |   1405   |已校对      |
|10. | Yates梵英词典                  | yat.json.gz                  |  44720   |            |
|11. | 于凌波唯识名词白话新解         | ylb.json                     |   1506   |            |
|12. | 朱芾煌《法相辭典》             | fxcd.json.gz                 |  14687   |            | 
|13. | 宋普潤法雲《翻譯名義集》       | fymyj.json.gz                |   1085   |            |
|14. | 宋，普濟《五燈會元》           | wdhy.json.gz                 |   2045   |            |
|15. | 《歷代名僧辭典》顧偉康編       | ldms.json.gz                 |   2121   |            |
|16. | 俗語佛源                       | syfy.json.gz                 |    566   |            |
|17. | 閱藏知津,明蕅益智旭撰顧偉康編輯| yzzj.json.gz                 |   1701   |            |
|18. | 《中华佛教百科全书》蓝吉富主编 | bkqs.json.gz                 |   6331   |  简体      |
|19. | 四分律名義標釋                 |                              |          |  待整理    |
|20. | 大智度论词典                   | dzdl.gls.txt                 |          |  待整理    |
|21. | 巴漢辭典    大馬比丘           | pali-dama.json               | 10530    |            |
|22. | 五譯合璧集要  鄭寶蓮           | pentaglot.json               |          |            |
|23. |  人名数据库                    |                              |          |            |
|24. |  地名数据库                    |                              |          |            |
|25. |ionary of Chinese Buddhist Terms| soothill-hodous              |          |            |
|26. | 正法華經詞典                   | dharmaraksa                  |          |            |
|27. | 妙法蓮華經詞典                 | kumarajiva                   |          |            |
|28. | 道行般若經詞典                 | lokaksema                    |          |            |
|29. | 比丘威儀法詞典                 | Abhisamacarika               |          |            |

## 浏览器兼容性
1. 主流浏览器: firefox、opera、chrome、safari、搜狗浏览器、IOS手机等主流浏览器都没有发现任何问题
2. 360浏览器在调整兼容性之后可以正常使用了。但是有些地方渲染比较奇怪
3. 微软系浏览器: Edge 12、ie11也可以翻页了，一切正常, 只是显示效果不理想
4. ie6已经确定无法使用, 不必尝试了; ie7没有测试过, 估计没戏; ie8已经可以使用了，只是导航条有些显示问题
5. 所有浏览器都只能使用xslt1.0版本语法,其中ie更有一些限制
6. firefox对勘误注释无法渲染为红色(anchor标签的问题); 也无法正常显示部分异体字, 会显示为对应的XML实体

| 浏览器        | 渲染引擎      | xslt版本| 
| ------------- |:-------------:| -------:| 
| 360           | Microsoft     |  1      |
| ie8           | Microsoft     |  1      |
| Edge          | Microsoft     |  1      |
| firefox       | Transformiix  |  1.0    |
| chrome        | libxslt       |  1.0    |
| opera         | libxslt       |  1.0    |
| safari(ios)   | libxslt       |  1.0    |
| safari(pc)    | libxslt       |  1.0    |
| 搜狗          | libxslt       |  1.0    |
| midori        | libxslt       |  1.0    |
| links2        |               |         |
| w3m           |               |         |
| lynx          |               |         |

## 操作系统兼容性
1. 对Linux、苹果都有良好的支持
2. 对Windows没有足够的测试，可能存在一些问题

## 编程语言兼容性
1. 不再支持Python3.9以下版本。

## 设备兼容性
1. 已经测试过的系统和设备列表: Ubuntu16.04、Ubuntu18.04、Ubuntu20.04、MacOS、苹果手机(4,5,se,5s,6s,8p,xr,12)、ipad mini(2,5)、ipad pro(11寸)、华为手机（部分型号）、文石note2、诺基亚N9


## TODO
- [x] 翻页, 上一页，下一页，经内分页功能, 转make_xml程序处理
- [x] 全文搜索
    - [x] 全文字搜索
    - [ ] 全文词搜索
    - [ ] 全文搜索的查询语法
    - [ ] 悉昙体的全文搜索, 使用拉丁字母搜索
- [ ] 删除悉昙字的图片，使用Unicode10.0的字来显现。目前字体做了一半  DONE!
- [ ] 删除蘭扎字的图片，暂时设想使用悉昙字的变体来实现
- [x] 对悉昙体叠辅音的支持, 由字库支持，暂时不做处理
- [ ] 登录用户
    - [ ] 对登录用户保存书签
    - [ ] 登录用户自定义css
    - [ ] 智能书签, 恢复上次阅读处: 每到新的段落就自动保存一次书签，以便保存书签的时候可以细化到段落
- [x] cb:tt标签X23n0438_004.xml应该显示全部汉字，然后显示一行悉曇字.有make_xml程序处理
- [ ] 回到顶部和回到底部的功能，在滚轮向上快速滚动时候出现向上箭头, 向下快速滚动时出现向下箭头，可以点击以便直接回到顶部或者回到底部
- [ ] 查字典词典的时候会和左边的超链接或者染色混淆 FIXME
- [ ] 导出pdf,docx,otf,html,epub,txt等多种格式文档
- [ ] 在点击简字进行简体转换的时候，停留在当前所浏览位置
- [ ] 对终端浏览器的支持
- [ ] 大藏经目录部文件的导航, 完成了一半
- [ ] 盲人模式，完全使用语音控制
- [ ] 字幕模式

## BUG-FIX
3. 浏览器只能使用xslt1.0版本, 无法做到跨文件目录跳转(没有base-uri() and document-uri()),解决方法: 在自生成的xml中，在cb:mulu中添加一个属性，内容为当前文件名
4. 在注释附近的字在查询字典的时候，会和注释链接到一起，导致显示不正常
5. 跨文件目录无法合并目录树，每个文件都单独显示目录树
6. firefox表格错位: B35n0194_001.xml
7. 佛光山词典多条解释的时候缺失解释
8. midori浏览器在p标签的内容换行时产生一个空格。应该在转换时候去掉回车
9. midori浏览器不支持CJK合字(暂时不需要此功能)
10. 所有浏览器都不支持200d合字. 终端和苹果手机支持
11. 使用byline cb:type="Author"表示作者, byline cb:type="translator"表示译者，混用大小写和中英文，还同时使用cb:jl_byline，含义模糊
12. p rend="inline" 的写法，本来就是一个行内元素,导致T55n2157_024.xml显示不正常
13. cbeta的note标注有时候显示的是勘误后的文字，有时候显示的是勘误前的文字。让人迷惑
14. ipadpro 无法显示生僻字

## 汉语拼音使用方式

1. 在方格內輸入漢語拼音並以數字 (1-4) 表示聲調，如：hua2。 （5 代表輕聲）
2. 可以「貼上」整段拼音，如：Pu3tong1hua4 Xue2xi2 Wang3。
3. 如要顯示 ü，請輸入 v5；如果要顯示 nǚ，請輸入 nv3。
4. 如要顯示 ê，請輸入 ea5。

## DEMO

1. 可以在 [美國DEMO1](http://45.76.171.153:8000) 看到演示效果 (暂时挂了)
2. 可以在 [香港DEMO2](http://cbeta.buddhism.org.hk) 看到演示效果

# 全文搜索使用的语法
1. 关键字是AND、OR、NOT。搜索域是title、author、content 可以随意组合,使用()
2. 例如搜索阿含经中的一段话,使用如下语句:  比丘集讲堂 AND title:阿含经

##  感谢与授权

此程序编写过程中得到了如下机构和个人的无私支持和帮助，表示衷心感谢！

1. cbeta 提供了最初的技术资料和持续不断的修改建议
2. 庄春江居士的阿含词典已经得到庄春江居士的(非營利用途)授权，但是此词典会持续更新，最新版在 [最新版本](http://agama.buddhason.org) 
3. [威廉梵英词典](https://github.com/sanskrit-lexicon/Cologne-Sanskrit-Tamil), from http://www.sanskrit-lexicon.uni-koeln.de/
4. [觉悟之路](http://dhamma.sutta.org/pali-course/Pali-Chinese-English%20Dictionary.html) 提供的15部巴利语词典: pali-hant.json.gz
5. 申月伟女士 编辑了大众阅藏目录
6. 微信公众号 梵明院 明泽先生 授权百字明咒语清唱音频
7. 苏长涛先生 制作佛经中所缺少的G区、H区、I区汉字的字体、制作兰扎体梵文字体、制作佛经缺字生僻字汉字字库(以上均为UNICODE 13.0标准版本)。建立在思源黑字形之上
8. 可善先生与香港佛教协会 为本阅读器DEMO在香港提供了一个新家
9. 释慧航法师 校勘丁福保《佛學大辭典》多处错误
10. 赵宇老师 提供金藏等多种校勘原始文本，提供校订用生僻字、异体字论文、字典、词典数十本；提供大正藏目录部文本
11. 蒋劲松老师 提供多处修改建议
12. 杨新宇博士 提供异译本对照目录
13. 大众阅藏网 提供了大部分经文朗读音频
14. 安得剑先生 校订了多音字发音表,校对多音字发音674字
16. 崔文治博士 校订了部分悉檀梵文
17. 悟修法师 提供了正字法校勘表
18. 比丘尼道葦 提供了多处异体字修正
19. 某匿名法师 协助将大正藏全部藏文文本化
20. 贤度法师 协助编写继续阅读功能，修改宣纸背景图片，使之无缝衔接
21. 郝莹莹女士团队() 协助获得大正藏日本部分，提供蔵経書院文庫1687部佛经
22. 康建国先生团队() 协助将大部分大正藏日本部分悉檀梵文的异体字进行了一遍校对，协助校对净土宗全书22万頁

##  捐助记录

1. 2018-08-21 22:23:00 收到Starful Night师兄6.88元 用于悉昙体字体开发
2. 2019-07-07 14:30:00 收到祖燈法师赠送文石BOOX Note2电纸书一部用于测试
3. 2021-11-28 08:29:00 收到宏开法师500.00元


##  联系方式 

1. 可以通过wenping_zhao@126.com与我联系使用中的问题, 提交BUG

2. 欢迎加入此项目!

