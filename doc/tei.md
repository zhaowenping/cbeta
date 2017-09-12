# CBETA TEI格式

## CBETA TEI格式(text部分)

## anchor标签

* anchor 标签表示锚点
* 封闭标签，无内容。在CBETA中经常链接到back部分的app、note和choice中，用来表示勘误
* 主要属性: @xml:id, @type; @type取值有star, cb-app, circle
* 问题是在xml中用两个封闭的标签来表示开始和结束。属性xml:id用beg开始表示起始，end开始表示结束。导致很难获得两个标签之间的文本内容

## byline 包含作品的主要责任陈述, 在cbeta中表示作者译者

* 主要属性@cb:type, 取值有author, Author, translater, Translater, 作者, 译者等，中文英文大小写混合
* 在文章中还经常使用cb:jl_byline, 应该是表示文章内的作者译者

## choice 对文章可替换的文字标记

* 子标签sic和corr联合使用；表示勘误
* 或者使用orig和reg联合使用。表示标准化，比如异体字替换为标准用字

## table 标签表示一个表格

* 子标签row和cell分别表示行和列

## g 标签表示非标准的文字或者字体

* 主要属性为@ref 链接到char标签的@xml:id属性, 由char标签指出这个文字或者字体的详细情况
* g标签现在的文本内容存在问题，经常使用的是这个字的PUA值。应该统一替换成unicode或者留空

## figure  图片

* 子标签graphic。graphic属性src描述了这个图片所在的位置

## form 词条

## lg 诗、偈、颂等韵文

* 子标签 l表示诗歌的一行
* 属性rend经常用来表示不正常的缩进,尤其是偈文以标点开头的情况

## list 表示列表项

* 子标签 item 表示列表中的一个项目

## cb:mulu 标签表示文章中的目录所在位置

* 没有属性诸如@xml:id指出这个位置
* cbeta采取的方式是手动编辑toc文件作为目录,感觉多此一举,本来应该可以自动生成的

## p 段落

* 属性@xml:id是标志段落的重要属性
* 有属性@rend的时候，@rend属性中存在inline的时候，很难正常显示这种行内段落

## cb:div

* 不知道为什么不用标准名字空间div1~div7，而要使用cb名字空间

## cb:yin 表示一个音节

* 子属性cb:sg和cb:zi. cb:zi经常表示咒语中应该放在一起表示一个字的多个字，比如: <cb:yin><cb:zi>得浪</cb:zi><cb:sg>二合</cb:sg></cb:yin>, 表示得浪应该做一个音节念出

## app

## note


## CBETA TEI格式(teiHeader部分)

## char 属性表示一个非标准的文字

* 位于路径/TEI/teiHeader/encodingDesc/charDecl/char
* 子标签charName和charProp、mapping
* charProp的子标签localName和value分别表示一个键值对。  localName的取值有normalized form、Character in the Siddham font、big5、composition、rjchar、Romanized form in CBETA transcription、Romanized form in Unicode transcription。
* normalized form表示被取代的通用字
* composition表示组字式
* Romanized form in CBETA transcription和Romanized form in Unicode transcription分别表示cbeta的拉丁表示和unicode的拉丁表示
* 其他localName取值分别表示采取那种覆盖方式来显示这个文字。皆不可取
* mapping子标签属性值@type, 取值有normal_unicode，unicode、PUA。其中unicode表示标签内容为unicode，normal_unicode表示通用字
* 属性xml:id如果SD开头表示是一个悉昙体，CB开头表示一个中文汉字，RJ开头表示是一个蘭扎体

# title 表示标题

* 位于/TEI/teiHeader/fileDesc/titleStmt/title


