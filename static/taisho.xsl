<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:cb="http://www.cbeta.org/ns/1.0"
    xmlns:str="http://exslt.org/strings"
    extension-element-prefixes="str"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs cb">
    <!--xpath-default-namespace="http://www.tei-c.org/ns/1.0"-->
    <!--xsl:import href="str.xsl"/-->
    <xsl:output method="html" encoding="utf-8" doctype-system="about:legacy-compat" indent="yes"/>

    <!--当前经集的名字, 形如: T20n1167 -->
    <xsl:variable name="current_sutra" select="/TEI[1]/@xml:id"/>
    <xsl:variable name="current_book" select="substring-before($current_sutra, 'n')"/>  <!--XXX T20-->
    <!--xsl:variable name="current_juan" select="substring-after($current_sutra, 'n')"/--> <!---1167-->
    <xsl:variable name="title" select="substring-after(substring-after(/TEI/teiHeader/fileDesc/titleStmt/title, 'No. '), ' ')"/>
    <xsl:variable name="copyright" select="/TEI/teiHeader/fileDesc/titleStmt/title[@xml:lang='zh-Hant']"/>
    <!--目录文件所在路径-->
    <xsl:variable name="toc_path" select="concat('/static/toc/', $current_book, '.toc')"/>
    <!--当前文件的卷数, 形如: 001; 目前只能靠猜了-->
    <!--xsl:variable name="juan" select="/TEI[1]/text/body//cb:juan[1]/@n|/TEI/text/body//milestone[@unit='juan']/@n|/TEI/text/body//cb:mulu[@type='卷']/@n"/-->
    <xsl:variable name="juan" select="format-number(/TEI/text/body//milestone[@unit='juan']/@n, '000')"/>
    <!--当前文件的语言, 默认繁体文言文-->
    <xsl:variable name="lang">
      <xsl:choose>
        <xsl:when test="/TEI/@xml:lang">
          <xsl:value-of select="/TEI/@xml:lang"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>lzh-Hant</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <!--是否属于疑伪部-->
    <!--xsl:variable name="fake">
        <xsl:variable name="nn" select="number(substring($current_juan, 1, 4))"/>
        <xsl:variable name="n2" select="($nn >= 8 and 15 >= $nn) or $nn = 31 or $nn = 43 or $nn = 63 or $nn = 64 or $nn = 69"/>
        <xsl:value-of select="starts-with($current_sutra, 'T85') or (starts-with($current_sutra, 'W') and $n2)"/>
    </xsl:variable-->

    <!--是否微软、火狐浏览器-->
    <xsl:variable name="MSIE" select="system-property('xsl:vendor')='Microsoft'"/>
    <xsl:variable name="firefox" select="system-property('xsl:vendor')='Transformiix'"/>

    <!--xsl:variable name="copyright">
        <xsl:choose>
        <xsl:when test="starts-with($current_sutra, 'T')">
            <xsl:text>《大正新脩大藏經》（大藏出版株式會社 ©）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'X')">
            <xsl:text>《卍新纂續藏經》（株式會社國書刊行會 ©）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'A')">
            <xsl:text>《趙城金藏》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'C')">
            <xsl:text>《中華藏》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'F')">
            <xsl:text>《房山石經》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'J')">
            <xsl:text>《嘉興大藏經》（新文豐出版公司）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'K')">
            <xsl:text>《高麗藏》（新文豐出版公司）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'L')">
            <xsl:text>《乾隆藏》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'M')">
            <xsl:text>《卍正藏經》（新文豐出版公司）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'P')">
            <xsl:text>《永樂北藏》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'S')">
            <xsl:text>《宋藏遺珍》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'U')">
            <xsl:text>《洪武南藏》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'D')">
            <xsl:text>國家圖書館善本佛典</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'N')">
            <xsl:text>《漢譯南傳大藏經》（元亨寺 ©）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'I')">
            <xsl:text>《北朝佛教石刻拓片百品》（中央研究院歷史語言研究所 ©）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'B')">
            <xsl:text>《大藏經補編》</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'GA')">
            <xsl:text>《中國佛寺史志彙刊》（杜潔祥主編）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'ZW')">
            <xsl:text>《藏外佛教文獻》（方廣錩 ©）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'GB')">
            <xsl:text>《中國佛寺志叢刊》（張智等編輯）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'Y')">
            <xsl:text>《印順法師佛學著作集》（印順文教基金會©）</xsl:text>
        </xsl:when>
        <xsl:when test="starts-with($current_sutra, 'G')">
            <xsl:text>《佛教大藏經》</xsl:text>
        </xsl:when>
        </xsl:choose>
    </xsl:variable-->

    <!--xml所在目录前缀, 形如: /xml/T01/-->
    <xsl:variable name="dir" select="concat('/xml/', substring-before($current_sutra, 'n'), '/')"/>

    <!--计算上一页-->
    <!--xsl:variable name="prev_filepath">
        <xsl:variable name="prevvol">
          <xsl:value-of select="concat($dir, $current_sutra, '_')"/>
          <xsl:number format="001" value="$juan - 1"/>
          <xsl:text>.xml</xsl:text>
        </xsl:variable>
    <xsl:if test="$MSIE or document($prevvol)">
        <xsl:value-of select="$prevvol"/>
    </xsl:if>
    </xsl:variable-->

    <!--计算下一页 TODO 太复杂了, 还是交给后台计算吧-->
    <!--xsl:variable name="next_filepath">
        <xsl:variable name="nextvol">
          <xsl:value-of select="concat($dir, $current_sutra, '_')"/>
          <xsl:number format="001" value="$juan + 1"/>
          <xsl:text>.xml</xsl:text>
        </xsl:variable>
        <xsl:variable name="nextsutra">
          <xsl:value-of select="concat($dir, substring-before($current_sutra, 'n'), 'n')"/>
          <xsl:number format="0001" value="substring-after($current_sutra, 'n') + 1"/>
          <xsl:text>_001.xml</xsl:text>
        </xsl:variable>
        <xsl:variable name="nexthan">
          <xsl:text>/xml/</xsl:text>
          <xsl:value-of select="substring(substring-before($current_sutra, 'n'), 1, 1)"/>
          <xsl:number format="01" value="substring(substring-before($current_sutra, 'n'), 2) + 1"/>
          <xsl:text>/</xsl:text>
          <xsl:value-of select="substring(substring-before($current_sutra, 'n'), 1, 1)"/>
          <xsl:number format="01" value="substring(substring-before($current_sutra, 'n'), 2) + 1"/>
          <xsl:text>n</xsl:text>
          <xsl:number format="0001" value="substring-after($current_sutra, 'n') + 1"/>
          <xsl:text>_001.xml</xsl:text>
        </xsl:variable>
        <xsl:choose>
          <xsl:when test="$MSIE or document($nextvol)">
              <xsl:value-of select="$nextvol"/>
          </xsl:when>
          <xsl:when test="$MSIE or document($nextsutra)">
              <xsl:value-of select="$nextsutra"/>
          </xsl:when>
          <xsl:when test="$MSIE or document($nexthan)">
              <xsl:value-of select="$nexthan"/>
          </xsl:when>
          <xsl:otherwise>
              <xsl:text>#</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
    </xsl:variable-->

    <!--开始页面根元素: 默认使用繁体文言文-->
    <xsl:template match="/">
        <html lang="{$lang}">
        <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no"/>
        <meta name="description" content="印刷品般的经典阅读"/>
        <meta name="keywords" content="大正藏, 中文, 排版, 排版規範, 阅藏, 大藏经"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <link rel="stylesheet" href="/static/bootstrap-3.3.7.min.css"/>
        <!--link rel="stylesheet" href="http://han-css.herokuapp.com/style.css"/-->
        <link rel="stylesheet" href="/static/jquery.webui-popover.min.css"/>
        <link rel="stylesheet" href="/static/tei.css"/>
        <!--link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Han/3.2.7/han.min.css"/-->
        <title>
            <xsl:value-of select="concat($current_sutra, ' ', $title)"/>
        </title>
        <script src="/static/jquery-3.3.1.min.js"></script>
        <script src="/static/bootstrap-3.3.7.min.js"></script>
        <script src="/static/jquery.webui-popover.min.js"></script>
        <!--script src="https://cdnjs.cloudflare.com/ajax/libs/Han/3.2.7/han.min.js"></script-->
        <!--[if lt IE9]> 
        <script src="http://cdn.staticfile.org/html5shiv/r29/html5.min.js"></script>
        <![endif]-->
        <script src="/static/my.js"></script>
        </head>
        <style type="text/css">
            @font-face {
                font-family: 'hanaminsat';
                src: url("<xsl:value-of select="concat('/static/fonts/', $current_sutra, '_', $juan, '.woff2')"/>") format("woff2"),
                url("<xsl:value-of select="concat('/static/fonts/', $current_sutra, '_', $juan, '.woff')"/>") format("woff");
            }
        </style>

        <!--firefox浏览器特有的菜单-->
        <body class="contenttext" contextmenu="supermenu">
            <!--header class="layout">
                <div><div class="logo">
                    <h1><a href="/manual/">漢字標準格式</a></h1>
                    <p class="desc">印刷品般的漢字排版框架</p>
                    </div>
                    <ul><li><a id="github-repo" href="https://github.com/ethantw/Han">GitHub Project</a></li>
                    <li><button id="trad2simp">繁簡切換</button></li></ul><button id="toggle-nav" hidden="">選單開關</button></div>
            </header-->

        <!--a href="#">&#128266;</a>
        <a href="https://www.sejda.com/html-to-pdf?save-link" target="_blank">Save to PDF</a-->
        <!--xsl:value-of select="function-available('codepoints-to-string')"/>
        <xsl:value-of select="function-available('str:tokenize')"/-->
        <!--xsl:value-of select="str:tokenize('2001-06-03T11:40:23', '-T:')"/-->

        <menu id="supermenu" type="context">
            <menuitem label="报告错误" onclick="alert('step1')"/>
            <menuitem label="保存书签" onclick="imageRotation('rotate-90')" icon="img/arrow-return-090.png"/>
            <menuitem label="拼音标注" onclick="alert('此功能暂时不开放')" icon="img/arrow-return-180.png"/>
            <menuitem label="简繁切换" onclick="alert('此功能暂时不开放')" icon="img/arrow-return-180.png"/>
            <menuitem label="横排竖排" onclick="alert('此功能暂时不开放')" icon="img/arrow-stop-180.png"/>
            <menuitem label="引用复制" onclick="alert('此功能暂时不开放')" icon="img/arrow-stop-270.png"/>
            <menuitem label="导出PDF"  onclick="alert('此功能暂时不开放')" icon="img/arrow-stop-270.png"/>
            <menuitem label="导出epub" onclick="alert('此功能暂时不开放')" icon="img/arrow-stop-270.png"/>
            <menuitem label="导出txt"  onclick="alert('此功能暂时不开放')" icon="img/arrow-stop-270.png"/>
        </menu>

            <!--ul class="pagination pagination-sm"-->
        <nav class="navbar navbar-default navbar-fixed-top justify-content-center" role="navigation">
            <!--div class="navbar-header">  
                <a class="navbar-brand">&#9776;</a>  
            </div--> 
            <!--div class="container"-->
                <!--ul id="pagination"></ul-->
                <ul class="navbar-nav">
                <li class="nav-item">
                    <!--a class="navbar-brand" href="/prev/{$current_sutra}_{$juan}/{$lang}">上一卷</a-->
                    <a class="navbar-link" href="/prev/{$current_sutra}_{$juan}">上一卷</a>
                </li>
                <li class="nav-item">
                    <a class="navbar-link" href="/mulu">目錄</a>
                </li>
                <li class="nav-item">
                    <!--a class="navbar-brand" href="/next/{$current_sutra}_{$juan}/{$lang}">下一卷</a-->
                    <a class="navbar-link" href="/next/{$current_sutra}_{$juan}">下一卷</a>
                </li>
            <!--input id="shupaictl" type="button" value="竖" onclick="shupai(this);"/-->
            <!--a id="pinyinctl" class="navbar-brand" onclick="pinyin(this);">P</a-->
                <li class="nav-item">
            <a class="nav-link">
                <xsl:attribute name="href">
                    <xsl:value-of select="concat('/zh_TW', $dir, $current_sutra, '_')"/>
                    <xsl:number format="001" value="$juan"/>
                    <xsl:text>.xml</xsl:text>
                </xsl:attribute>
                正
            </a>
                </li>
                <li class="nav-item">
            <a class="nav-link">
                <xsl:attribute name="href">
                    <xsl:value-of select="concat('/zh', $dir, $current_sutra, '_')"/>
                    <xsl:number format="001" value="$juan"/>
                    <xsl:text>.xml</xsl:text>
                </xsl:attribute>
                简
            </a>
                </li>
            </ul>
            <!--form class="collspae navbar-collspae navbar-form navbar-left" role="search">
               <div class="form-group">
                  <input type="search" class="form-control" placeholder="Search"/>
               </div>
               <button type="submit" class="btn btn-default">直达</button>
            </form-->    
            <!--/div-->
        </nav>

        <!--侧边栏目录 max(level)=28-->
        <nav>
            <ul class="toc">
            <!--Affix附加导航-->
            <!--ul class="nav nav-tabs nav-stacked" data-spy="affix" data-offset-top="125"-->
            <!--生成目录-->
                <!--xsl:with-param name="pos" select="document($prev_filepath)//cb:mulu|//cb:mulu|document($next_filepath)//cb:mulu"/-->
            <!--xsl:call-template name="make_catalog">
                <xsl:with-param name="pos" select="//cb:mulu"/>
            </xsl:call-template-->
            </ul>
        </nav>

            <br/>

        <div id="topAnchor"/>
        <a href="#topAnchor" style="position:fixed;right:0;bottom:0" rel="bookmark">&#x21c8;</a>  <!--回到顶部-->
        <a href="#bottomAnchor" style="position:fixed;right:0;top:70" rel="bookmark">&#x21ca;</a> <!--回到底部-->
        <div id="allcontent" class="content"> <!-- style="writing-mode:vertical-rl;"-->
        <!--补上南传等经典的标题以及作者-->
        <xsl:if test="not(//cb:jhead)">
            <h1 class="title">
                <xsl:value-of select="concat($current_sutra, ' ', $title)"/>
            </h1>
            <br/>
            <div class="byline">
                <xsl:value-of select="/TEI/teiHeader/fileDesc/titleStmt/author"/>
            </div>
            <br/>
            <br/>
        </xsl:if>
        <!--span>写<span>好&#x20de;很</span>写&#x20dd;</span-->

            <!--div class="span2 col-xs-12 col-sm-3 col-md-2 navbar-inverse">
                <ul class="nav nav-pills nav-stacked">
                    <li class="active"><a href="#">Home</a></li>
                    <li><a href="#">Tutorials</a></li>
                    <li><a href="#">Practice Editor </a></li>
                    <li><a href="#">Gallery</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </div-->

        <!--左侧目录-->
        <!--xsl:copy-of select="document(concat('/static/toc/', $current_book, '.xml'))"/-->
        <!--xsl:copy-of select="document('/static/t.xml')"/-->
        <div style="height:40px">
        </div>
              <audio controls="controls" preload="meta" style="width:100%">
                <source type="audio/mp4">
                  <xsl:attribute name="src">      
                      <xsl:value-of select="concat('/static/m4a/', $current_sutra, '_', $juan,'.m4a')"/>
                  </xsl:attribute>
                </source>
                <source type="audio/mpeg">
                  <xsl:attribute name="src">      
                      <xsl:value-of select="concat('/static/mp3/', $current_sutra, '_', $juan,'.mp3')"/>
                  </xsl:attribute>
                </source>
              </audio>
        <!--正文内容-->
        <div class="contentx">
            <xsl:apply-templates/>
        </div>
        <div id="bottomAnchor"/>
        <!--版權資訊-->
        <div>
            <hr style=" height:2px;border:none;border-top:2px solid #185598;" />
            <!--div>【經文資訊】<xsl:value-of select="$copyright"/> 第 <xsl:value-of select="concat(substring-before($current_sutra, 'n'), ' 冊 No. ', substring-after($current_sutra, 'n'), ' ', $title)"/><br/-->
            <div>【經文資訊】<xsl:value-of select="$copyright"/> 第 <xsl:value-of select="concat(substring-before($current_sutra, 'n'), ' 冊')"/><br/>
                <!--【版本記錄】CBETA 電子佛典 2016.06，完成日期：2016/06/15 <br/>
            【編輯說明】本資料庫由中華電子佛典協會（CBETA）依卍新續藏所編輯 <br/>
            -->
            【原始資料】<xsl:value-of select="/TEI/teiHeader/encodingDesc/projectDesc/p[@xml:lang='zh']"/><br/>
            【其他事項】本資料庫可自由免費流通，詳細內容請參閱【中華電子佛典協會資料庫版權宣告】 </div>
            <hr style=" height:2px;border:none;border-top:2px solid #185598;" />
        </div>

        <!--底栏目录-->
        <nav class="navbar-sm navbar-default" role="navigation">
            <ul class="nav navbar-nav">
             <li>
                <!--a class="navbar-brand" href="/prev/{$current_sutra}_{$juan}/{$lang}">上一卷</a-->
                <a class="navbar-brand" href="/prev/{$current_sutra}_{$juan}">上一卷</a>
             </li>
             <li>
                <a href="/mulu">返回目录</a>
             </li>
             <li>
                <!--a class="navbar-brand" href="/next/{$current_sutra}_{$juan}/{$lang}">下一卷</a-->
                <a class="navbar-brand" href="/next/{$current_sutra}_{$juan}">下一卷</a>
             </li>
             </ul>
        </nav>
    </div>

        </body>
        </html>
    </xsl:template>

    <!--处理整体结构: TEI\teiHeader\app-->

    <!--xsl:template match="TEI">
        <xsl:apply-templates/>
    </xsl:template-->

    <xsl:template match="teiHeader"/>

    <!--不显示back部分-->
    <xsl:template match="text/back">
    </xsl:template>

    <!--不能切换段落, 否则显示不正常-->
    <xsl:template match="pb">
        <!--a>
          <xsl:attribute name="id">
            <xsl:value-of select="@xml:id"/>
          </xsl:attribute>
          <xsl:attribute name="href">
              <xsl:value-of select="concat('/static/img/00', substring(@xml:id, 10, 4), '.jpg')"/>
          </xsl:attribute>
          &#x1F5BB;
        </a-->
    </xsl:template>

    <!--不在正文显示目录-->
    <xsl:template match="cb:mulu">
        <a class="mulu">
           <xsl:attribute name="id">
               <xsl:value-of select="generate-id()"/>
           </xsl:attribute>
        </a>
    </xsl:template>


    <!--处理表格table-->
    <!--TODO: table rend="border:0"-->
    <xsl:template match="table">
        <table class="table table-bordered">
            <xsl:apply-templates/>
        </table>
    </xsl:template>

    <!--处理表格row-->
    <xsl:template match="row">
        <tr>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>

    <!--处理表格cell FIXME: firefox表格錯位-->
    <xsl:template match="cell">
        <td>
            <xsl:if test="@cols">
            <xsl:attribute name="colspan">
                <xsl:value-of select="@cols"/>
            </xsl:attribute>
            </xsl:if>
            <xsl:if test="@rows">
            <xsl:attribute name="rowspan">
                <!--xsl:if test="$firefox">
                <xsl:value-of select="@rows+1"/>
                </xsl:if>
                <xsl:if test="not($firefox)"-->
                <xsl:value-of select="@rows"/>
                <!--/xsl:if-->
            </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </td>
    </xsl:template>

    <!--处理所有的颂-->
    <!-- rend="margin-left:1em;text-indent:-1em" -->
    <xsl:template match="lg">
        <div class="lg">
            <xsl:if test="@xml:id">
                <xsl:attribute name="id">
                    <xsl:value-of select="@xml:id"/>
                </xsl:attribute>
            </xsl:if>
         <xsl:attribute name="class">
           <xsl:choose>
           <xsl:when test="starts-with(child::l[1], '「『')">
             <xsl:text>lll</xsl:text>
           </xsl:when>
           <xsl:when test="starts-with(child::l[1], '「') or starts-with(child::l[1], '“') or starts-with(child::l[1], '∴')">
             <xsl:text>ll</xsl:text>
           </xsl:when>
           <xsl:otherwise>
               <xsl:text>lg</xsl:text>
           </xsl:otherwise>
           </xsl:choose>
         </xsl:attribute>
            <!--xsl:choose>
                <xsl:when test="@rend">
                    <xsl:attribute name="style">
                    <xsl:value-of select="concat('text-indent:', substring-before(substring-after(@rend,'text-indent:'), 'em'), 'em;')"/>
                    </xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                </xsl:otherwise>
            </xsl:choose-->
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!--偈中重复的换行只显示一个换行-->
    <xsl:template match="lg/lb">
        <xsl:if test="local-name(preceding-sibling::*[1])!='lb'">
            <br/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="lb[@type='honorific']">
        <br/>
    </xsl:template>

    <xsl:template match="lb">
        <!--span class="lb">
          <xsl:attribute name="id">
            <xsl:value-of select="@n"/>
          </xsl:attribute>
        </span-->
    </xsl:template>

    <xsl:template match="lg/l">
       <span class="l">
         <!--xsl:attribute name="class">
           <xsl:choose>
             <xsl:when test="@rend='Alignr'">
               <xsl:text>right</xsl:text>
             </xsl:when>
             <xsl:when test="@rend='Alignc'">
               <xsl:text>center</xsl:text>
             </xsl:when>
             <xsl:when test="starts-with(@rend,'text-indent:')">
               <xsl:text>indent</xsl:text>
               <xsl:value-of select="substring-before(substring-after(@rend,':'),'em')" />
             </xsl:when>
             <xsl:when test="starts-with(@rend,'indent(')">
               <xsl:text>indent</xsl:text>
               <xsl:value-of select="substring-before(substring-after(@rend,'('),')')" />
             </xsl:when>
             <xsl:when test="@rend='indent'">
               <xsl:text>indent1</xsl:text>
             </xsl:when>
             <xsl:otherwise>
               <xsl:text>l</xsl:text>
             </xsl:otherwise>
           </xsl:choose>
         </xsl:attribute-->
         <xsl:apply-templates/>
     </span>
    </xsl:template>

    <!--清除文档中无用空格, 替换错误的人名分割符号-->
    <xsl:template match="text()|@*">
        <!--xsl:value-of select="translate(normalize-space(.), '&#xff0e;', '&#x00b7;')"/-->
        <xsl:value-of select="normalize-space(.)"/>
            <!--xsl:call-template name="zhuyin">
                <xsl:with-param name="string" select="."/>
            </xsl:call-template-->
    </xsl:template>

    <!--处理图片-->
    <xsl:template match="figure">
        <figure>
          <xsl:apply-templates/>
          <figcaption>
            <xsl:value-of select="head"/>
          </figcaption>
        </figure>
    </xsl:template>

    <xsl:template match="graphic">
      <img class="img-responsive">
        <xsl:attribute name="src">
            <xsl:text>/static</xsl:text>
            <xsl:value-of select="substring(@url, 3)"/>
        </xsl:attribute>
      </img>
    </xsl:template>

    <!--处理段落-->
    <!--xsl:template match="p[contains(@rend, 'inline')]">
        <span><xsl:apply-templates/></span>
    </xsl:template-->

    <!--xsl:template match="p[@cb:type='dharani']/lb">
        <xsl:if test="local-name(preceding-sibling::*[1])!='lb'">
            <br/>
        </xsl:if>
    </xsl:template-->

    <xsl:template match="p[contains(@cb:type, 'head')]">
        <xsl:variable name="hunit" select="concat('h', substring(@cb:type, 5)+1)"/>
        <xsl:element name="{$hunit}">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <!--咒语段落, 分成悉昙体和汉语两个段落表现 -->
    <!--xsl:template match="p[@cb:type='dharani']">
        <p class="dharani">
            <xsl:apply-templates/>
        </p>
    </xsl:template-->

    <!--XXX-->
    <xsl:template match="cb:t[@xml:lang='zh-x-yy']">
        [<xsl:apply-templates/>]
    </xsl:template>

    <xsl:template match="p[@cb:type='dharani']">
        <xsl:choose>
        <xsl:when test="not(cb:tt)">
            <xsl:if test="@xml:id">
              <audio controls="controls" preload="meta">
                <source type="audio/mp4">
                  <xsl:attribute name="src">      
                      <xsl:value-of select="concat('/static/m4a/', @xml:id, '.m4a')"/>
                  </xsl:attribute>
                </source>
              </audio>
            </xsl:if>
            <p class="dharani">
              <xsl:apply-templates/>
            </p>
        </xsl:when>
        <xsl:when test="cb:tt[@place='inline']">
            <p class="dharani">
              <span lang="sa-Sidd"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-Sidd']"/></span>
              <!--span lang="sa-Sidd"><xsl:apply-templates select="starts-with(cb:tt/cb:t[@xml:lang], 'sa')"/></span-->
              <span lang="sa-x-rj"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-x-rj']"/></span>
              <span>(<xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-Hant']"/>)</span>
              <!--span lang="zh-Hant">(<xsl:apply-templates select="starts-with(cb:tt/cb:t[@xml:lang], 'zh')"/>)</span-->
              <!--span lang="zh-Hant">(<xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-x-yy']"/>)</span-->
              <xsl:apply-templates/>
            </p>
        </xsl:when>
        <xsl:otherwise>
            <p lang="sa-Sidd" class="dharani"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-Sidd']"/></p>
            <p lang="sa-x-rj" class="dharani"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='sa-x-rj']"/></p>
            <p class="dharani"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-Hant']"/></p>
            <!--p lang="zh-Hant" class="dharani"><xsl:apply-templates select="cb:tt/cb:t[@xml:lang='zh-x-yy']"/></p-->
        </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="p[@cb:type='pre']">
        <pre>
          <xsl:value-of select="."/>
        </pre>
    </xsl:template>

    <xsl:template match="p">
        <p> <!--lang="lzh-Hant"-->
          <xsl:if test="@xml:id">
              <xsl:attribute name="id">      
                <xsl:value-of select="@xml:id"/>
              </xsl:attribute>
          </xsl:if>
          <xsl:apply-templates/>
        </p>
    </xsl:template>

    <!--处理词典-->
    <xsl:template match="entry"><dl><xsl:apply-templates/></dl></xsl:template>
    <xsl:template match="form"><dt><xsl:apply-templates/></dt></xsl:template>
    <xsl:template match="cb:def"><dd><xsl:apply-templates/></dd></xsl:template>

    <!--处理note-->
    <xsl:template match="note[@place='inline']|note[@type='inline']">
        <span class="note">(<xsl:apply-templates/>)</span>
    </xsl:template>

    <xsl:template match="space">
      <span style="display:inline-block">
        <xsl:if test="@quantity">
          <xsl:variable name="unit">
            <xsl:choose>
              <xsl:when test="@unit='chars'">
                <xsl:text>em</xsl:text>
              </xsl:when>
              <xsl:when test="@unit">
                <xsl:value-of select="@unit"/>
              </xsl:when>
              <xsl:otherwise>em</xsl:otherwise>
            </xsl:choose>
          </xsl:variable>
          <xsl:attribute name="width">
            <xsl:value-of select="@quantity"/>
            <xsl:value-of select="$unit"/>
          </xsl:attribute>
        </xsl:if>
      </span>
    </xsl:template>


    <!--添加专名号: 人名、地名、朝代名、种族名、国名、机构名-->
    <xsl:template match="name">
        <span class="person">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

  <!--xsl:template match="juan">
          <xsl:apply-templates/>
  </xsl:template-->
    <!--连续的cb:tt标签在最后一次性显示 TODO-->

    <!--xsl:template match="cb:tt">
        <ruby>
            <xsl:apply-templates/>
        </ruby>
    </xsl:template>
    <xsl:template match="cb:t[@xml:lang='zh']">
        <rb>
            <xsl:apply-templates/>
        </rb>
    </xsl:template>
    <xsl:template match="cb:t[@xml:lang!='zh']">
        <rt>
            <xsl:apply-templates/>
        </rt>
    </xsl:template-->

    <!--TODO 需要使用rtc修改成三行-->
            <!--zh-x-yy-->
    <!--xsl:template match="cb:tt">
        <ruby>
        <rb>
            <xsl:if test="cb:t[@xml:lang='zh']">
                <xsl:apply-templates select="cb:t[@xml:lang='zh']"/>
            </xsl:if>
            <xsl:if test="cb:t[@xml:lang='sa-Sidd']">
                <xsl:apply-templates select="cb:t[@xml:lang='sa-Sidd']"/>
            </xsl:if>
            <xsl:if test="cb:t[@xml:lang='sa-x-rj']">
                <xsl:apply-templates select="cb:t[@xml:lang='sa-x-rj']"/>
            </xsl:if>
            <xsl:if test="cb:t[@xml:lang='sa']">
                <xsl:apply-templates select="cb:t[@xml:lang='sa']"/>
            </xsl:if>
        </rb>
        <rt>
            <xsl:apply-templates select="cb:t[@xml:lang='sa-Latn']"/>
        </rt>
        </ruby>
    </xsl:template-->

    <!--xsl:template match="cb:t/g">
        <xsl:apply-templates select="key('char_id', substring(@ref, 2))/charProp[localName='Romanized form in Unicode transcription']/value"/>
    </xsl:template-->

    <!--xsl:template match="cb:tt">
        <xsl:variable name="header" select="generate-id(.)"/>
        <xsl:variable name="prev_node" select="preceding-sibling::*[1]"/>
        <xsl:variable name="next_node" select="following-sibling::*[1]"/>
        <xsl:if test="local-name($prev_node)!='tt'">
            <xsl:apply-templates select="cb:t[@xml:lang!='zh']"/>
            <xsl:for-each select="following-sibling::cb:tt"> 
                    <xsl:apply-templates select="cb:t[@xml:lang!='zh']"/>
                <xsl:if test="generate-id(preceding-sibling::cb:tt[1])=$header"> 
                </xsl:if>
                </xsl:for-each-->

            <!--xsl:apply-templates select="cb:t[@xml:lang!='zh']"/>
            <xsl:if test="local-name($next_node)='tt'">
                <xsl:for-each select="following-sibling::cb:tt[generate-id(preceding-sibling::*[1])=$header]"> 
                    <xsl:apply-templates select="cb:t[@xml:lang!='zh']"/>
                </xsl:for-each-->
                    <!--xsl:if test="count(following-sibling::*)=count(following-sibling::cb:tt)">
                    </xsl:if-->
                    <!--xsl:value-of select="generate-id(current())=generate-id(preceding-sibling::*[1])"/-->
                    <!--xsl:value-of select="local-name(preceding-sibling::*[1])"/-->
                <!--xsl:call-template name="tt" select="$next_node">
                    <xsl:with-param name="nn" select="$next_node"/>
                </xsl:call-template-->
            <!--/xsl:if-->
            <!--xsl:value-of select="local-name(following-sibling::*[1])"/>
            <xsl:value-of select="local-name(preceding-sibling::*[1])"/>
            <xsl:call-template name="tt" select="preceding-sibling::*[1]">
                <xsl:with-param name="ntext" select="cb:t[@xml:lang!='zh']"/>
            </xsl:call-template-->
        <!--/xsl:if>
        <xsl:apply-templates select="cb:t[@xml:lang='zh']"/>
    </xsl:template-->

    <!--sa,sa-x-rj,sa-Sidd多语言对照 -->
    <!--xsl:template match="cb:t">
        <xsl:if test="@xml:lang='zh'">
            <xsl:apply-templates/>
        </xsl:if>
        <xsl:if test="@xml:lang!='zh'">
            <span style="color:#A9A9A9"><xsl:apply-templates/></span>
        </xsl:if>
    </xsl:template-->

    <!--处理异体字-->
    <xsl:key name="char_id" match="char" use="@xml:id"/>
    <xsl:template match="g">
        <xsl:variable name="Ref" select="substring(@ref, 2)"/>
        <xsl:variable name="char" select="key('char_id', $Ref)"/>
    <!--localName>normalized form</localName>
    <localName>Character in the Siddham font</localName>   xml:id="SD-E2F6"
    <localName>big5</localName>                            xml:id="SD-E2F6"
    <localName>composition</localName> 组字式              xml:id="CB00178"
    <localName>rjchar</localName>                          xml:id="RJ-CBD3"
    <localName>Romanized form in CBETA transcription</localName>
    <localName>Romanized form in Unicode transcription</localName>
    <mapping type="normal_unicode">U+2A31C</mapping-->
    <xsl:choose>
        <!--悉檀字-->
        <xsl:when test="starts-with($Ref, 'SD')">
        <span lang="sa-Sidd" class="gaiji_sd">
            <ruby>
            <!--xsl:value-of select="."/-->
            <xsl:choose>
                <xsl:when test="$char/mapping[@type='unicode']">
                    <xsl:value-of select="$char/mapping[@type='unicode']"/>
                    <!--span class="gaiji_sd">
                        <xsl:value-of select="."/>
                    </span-->
                </xsl:when>
                <xsl:otherwise>
                <img>
                <xsl:attribute name="src">
                    <xsl:text>/static/sd-gif/</xsl:text>
                    <xsl:value-of select="substring($Ref, 4, 2)"/>
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="$Ref"/>
                    <xsl:text>.gif</xsl:text>
                </xsl:attribute>
                </img>
                </xsl:otherwise>
            </xsl:choose>
            <!--装cbeta字库用这句, 没装用上面的图片-->
            <!--xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='Character in the Siddham font']/value"/-->
                <rt lang="sa-Latn">
                    <xsl:value-of select="key('char_id', $Ref)/charProp[localName='Romanized form in Unicode transcription']/value"/>
                </rt>
            </ruby>
        </span> 
        </xsl:when>

        <!--蘭札字-->
        <xsl:when test="starts-with($Ref, 'RJ')">
        <span lang="sa-x-rj" class="gaiji_rj">
            <ruby>
            <xsl:choose>
                <xsl:when test="$char/mapping[@type='unicode']">
                    <xsl:value-of select="$char/mapping[@type='unicode']"/>
                </xsl:when>
                <xsl:otherwise>
                <img>
                <xsl:attribute name="src">
                    <xsl:text>/static/rj-gif/</xsl:text>
                    <xsl:value-of select="substring($Ref, 4, 2)"/>
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="$Ref"/>
                    <xsl:text>.gif</xsl:text>
                </xsl:attribute>
                </img>
                </xsl:otherwise>
            </xsl:choose>
            <!-- 安装了cbeta的蘭扎字库，使用这句，不推荐-->
            <!--xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='rjchar']/value"/-->
                <rt lang="sa-Latn">
                    <xsl:value-of select="key('char_id', $Ref)/charProp[localName='Romanized form in Unicode transcription']/value"/>
                </rt>
            </ruby>
        </span> 
        </xsl:when>

        <!--組字式-->
        <xsl:when test="starts-with($Ref, 'CB')">
        <!--span class="gaiji_cb"-->
            <!--abbr title="xxxxx"-->
            <xsl:variable name="term1" select=".."/>
            <xsl:variable name="nor" select="$char/charProp[localName='normalized form']/value"/>
            <xsl:choose>
            <xsl:when test="$char/mapping[@type='unicode']">
                <span class="gaiji_uni">
                    <xsl:value-of select="."/>
                </span>
            </xsl:when>
            <!--使用xml实体输出显示，不能用于搜索,ff无效, 形如: &#x25F9D;-->
            <xsl:when test="$char/mapping[@type='normal_unicode']">
                <span class="gaiji_nun">
                    <!--xsl:value-of disable-output-escaping='yes' select="concat('&amp;#x', substring($char/mapping[@type='normal_unicode'], 3), ';')"/-->
                    <xsl:value-of select="."/>
                </span>
            </xsl:when>
            <xsl:when test="$nor and not($term1[@rend='no_nor'])">
                <!--span class="gaiji_nor"><xsl:value-of select="$nor"/></span-->
                <span class="gaiji_nor"><xsl:value-of select="."/></span>
            </xsl:when>
            <xsl:when test="$char/charProp[localName='composition']/value">
                <span class="gaiji_nor">
                    <xsl:value-of select="$char/charProp[localName='composition']/value"/>
                </span>
            </xsl:when>
            </xsl:choose>
            <!--/abbr-->
        <!--/span--> 
        </xsl:when>
      </xsl:choose>
    </xsl:template>

    <!--处理teiHeader-->
    <xsl:template match="titleStmt/title">
      <xsl:if test="preceding-sibling::title">
        <br/>
      </xsl:if>
      <xsl:apply-templates/>
    </xsl:template>

    <!--head 小节的目录。上级节点是div类节点则不显示? -->
    <xsl:template match="head">
      <xsl:variable name="parent" select="local-name(..)"/>
      <!--xsl:if test="not(starts-with($parent,'div'))">
        <xsl:apply-templates/>
      </xsl:if-->
      <h2 class="head">
        <xsl:apply-templates/>
      </h2>
    </xsl:template>

  <!--xsl:template match="title">
      <h1 class="title"><xsl:value-of select="."/></h1>
    <br/>
  </xsl:template-->

    <!--标题 type=X, pin-->
    <xsl:template match="cb:jhead">
        <h1 class="title">
            <xsl:apply-templates/>
        </h1>
        <!--br/-->
    </xsl:template>

    <!--最后一个作者译者cb:type="author"之后空出两行然后开始正文-->
    <xsl:template match="byline">
        <div class="byline">
            <xsl:apply-templates/>
        </div>
        <xsl:if test="../byline[last()]=.">
         <br/>
         <br/>
        </xsl:if>
    </xsl:template>

    <!--列表中的作者译者不另外换行,应该清洗掉这种标志 XXX-->
    <xsl:template match="list//byline|cb:jl_byline">
        <span class="byline">
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
   <!--处理列表-->
   <xsl:template match="list"><ul><xsl:apply-templates/></ul></xsl:template>
   <xsl:template match="list/item"><li><xsl:apply-templates/></li></xsl:template>

    <!--处理空缺 unclear@reason-->
    <xsl:template match="unclear">
        <span class="unclear">
            <xsl:text>&#x258a;</xsl:text>
        </span>
    </xsl:template>

    <!--使用popover显示注释, 链接三个标签，可能有些不对 TODO 使用超链接-->
    <!--跨文件注释？note type="cf1">K19n0663_p0486b18</note-->
    <!--note type="cf2">T02n0099_p0285c29</note-->
    <!--note n="0283003" type="cf." place="foot" target="#nkr_note_cf._0283003">[No. 100(20)]</note-->
    <xsl:template match="note[starts-with(@type, 'cf')]">
        (見:<a><xsl:value-of select="."/></a>)
    </xsl:template>
    <!--xsl:template match="reg">
    </xsl:template-->

    <xsl:template match="orig">
        <xsl:apply-templates/>
        <xsl:text>&#8658;</xsl:text>
    </xsl:template>

    <!--lem是版本, corr是勘误-->
    <xsl:template match="lem|corr">
        <xsl:apply-templates/>
        <xsl:if test="@wit">
            <xsl:call-template name="tokenize">
                <xsl:with-param name="string" select="@wit"/>
            </xsl:call-template>
        </xsl:if>
        <xsl:text>&#8656;</xsl:text>
    </xsl:template>

    <xsl:template match="rdg|sic">
        <xsl:apply-templates/>
        <xsl:if test="@wit">
            <xsl:call-template name="tokenize">
                <xsl:with-param name="string" select="@wit"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

    <!--比较危险的用法,可能报错: 给替换的部分着红色-->

    <xsl:key name="tt_from" match="cb:tt" use="@from"/>
    <xsl:key name="app_from" match="app" use="@from"/>
    <xsl:key name="choice_from" match="choice" use="@cb:from"/>
    <xsl:key name="note_target" match="note" use="@target"/>
    <xsl:key name="note_n" match="note" use="@n"/>
    <xsl:key name="witness_id" match="witness" use="@xml:id"/>

    <xsl:template match="anchor">
        <xsl:variable name="Ref" select="concat('#', @xml:id)"/>
        <!--注释使用花青色-->
        <xsl:if test="not($firefox) and starts-with(@xml:id, 'beg')">
            <xsl:text disable-output-escaping="yes">&lt;span style="color:red"&gt;</xsl:text>
        </xsl:if>
        <xsl:if test="not($firefox) and starts-with(@xml:id, 'end')">
            <xsl:text disable-output-escaping="yes">&lt;/span&gt;</xsl:text>
        </xsl:if>
        <sup lang="en">
        <span data-toggle="popover" data-placement="auto" data-container="body" data-trigger="hover focus">
        <!--a data-toggle="popover" data-placement="auto" data-trigger="hover"-->
        <xsl:if test="@xml:id">
            <xsl:attribute name="id">
                <xsl:value-of select="@xml:id"/>
            </xsl:attribute>
        </xsl:if>
        <xsl:choose>
            <xsl:when test="@type='cb-app' and key('app_from', $Ref)">
            <!--xsl:when test="key('app_from', $Ref)"-->
                <xsl:attribute name="data-title">
                    <!--xsl:text>CBETA修訂註解</xsl:text-->
                    <xsl:value-of select="key('app_from', $Ref)/../../head"></xsl:value-of>
                </xsl:attribute>
                <xsl:attribute name="data-content">
                    <xsl:apply-templates select="key('app_from', $Ref)"/>
                </xsl:attribute>
                <xsl:value-of select="concat('[c', substring(@xml:id, 5), ']')"/>
            </xsl:when>
            <xsl:when test="@type='cb-app' and key('choice_from', $Ref)/sic">
                <xsl:attribute name="data-title">
                    <!--xsl:text>勘誤</xsl:text-->
                    <xsl:value-of select="key('choice_from', $Ref)/../../head"></xsl:value-of>
                </xsl:attribute>
                <xsl:attribute name="data-content">
                    <!--xsl:apply-templates select="key('choice_from', $Ref)"/-->
                    原文為: <xsl:apply-templates select="key('choice_from', $Ref)/sic"/>
                </xsl:attribute>
                <xsl:value-of select="concat('[c', substring(@xml:id, 5), ']')"/>
            </xsl:when>
            <xsl:when test="@type='cb-app' and key('choice_from', $Ref)/reg">
                <xsl:attribute name="data-title">
                    <xsl:apply-templates select="key('choice_from', $Ref)/reg/@type"/>  <!--通用詞-->
                </xsl:attribute>
                <xsl:attribute name="data-content">
                    <xsl:apply-templates select="key('choice_from', $Ref)"/>
                </xsl:attribute>
                <xsl:value-of select="concat('[c', substring(@xml:id, 5), ']')"/>
            </xsl:when>
            <xsl:when test="@type='star' and key('app_from', $Ref)">
                <xsl:attribute name="data-title">
                    <!--xsl:text>註解</xsl:text-->
                    <xsl:value-of select="key('app_from', $Ref)/../../head"></xsl:value-of>
                </xsl:attribute>
                <xsl:attribute name="data-content">
                    <xsl:apply-templates select="key('app_from', $Ref)"/>,
                    <!--xsl:variable name="tmp" select="substring(key('app_from', $Ref)/@corresp, 2)"/>
                    <xsl:apply-templates select="key('note_n', $tmp)"/-->
                </xsl:attribute>
                <xsl:text>[*]</xsl:text>
            </xsl:when>
            <xsl:when test="key('note_target', $Ref)">
                <xsl:attribute name="data-title">
                    <!--xsl:text>註釋xx</xsl:text-->
                    <xsl:value-of select="key('note_target', $Ref)/../../head"></xsl:value-of>
                </xsl:attribute>
                <xsl:attribute name="data-content">
                    <xsl:apply-templates select="key('note_target', $Ref)"/>
                </xsl:attribute>
                <xsl:value-of select="concat('[', substring(@n, 6), ']')"/>
            </xsl:when>
            <xsl:when test="@type='circle'">
            </xsl:when>
        </xsl:choose>
        </span>
        </sup>
    </xsl:template>


    <!--处理div 折叠式注释 TODO, 里面的异体字处理有些问题D47n8936_002-->
    <!--xsl:template match="cb:div[@type='orig']"-->
    <xsl:template match="cb:div[@type='commentary']">
        <div class="commentary panel-collapse">
            <a data-toggle="collapse" data-parent="#accordion" href="#{generate-id()}"><span class="caret"/>註疏：</a>
            <div id="{generate-id()}" class="panel-collapse collapse">
              <div class="panel-body">
                <xsl:apply-templates/>
              </div>
            </div>
        </div>
        <br/>
    </xsl:template>


    <!--生成导航目录 max(cb:mulu@level)=28, XXX: 不能显示cb:mulu中的异体字:K34n1257_007.xml-->
    <xsl:template name="make_catalog">
        <xsl:param name="pos"/> 
        <xsl:for-each select="$pos">
        <xsl:choose>
            <xsl:when test="@level=1">
                <li class="toc"><a>
                    <xsl:attribute name="href">
                        <xsl:text>#</xsl:text>
                        <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
                    </xsl:attribute>
                    <xsl:value-of select="."/>
                </a></li>
            </xsl:when>
            <xsl:when test="@level=2">
                <ul><li><a>
                    <xsl:attribute name="href">
                    <xsl:text>#</xsl:text>
                        <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
                    </xsl:attribute>
                    <xsl:value-of select="."/>
                </a></li></ul>
            </xsl:when>
            <xsl:when test="@level=3">
                <ul><ul><li><a>
                    <xsl:attribute name="href">
                    <xsl:text>#</xsl:text>
                        <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
                    </xsl:attribute>
                    <xsl:value-of select="."/>
                </a></li></ul></ul>
            </xsl:when>
            <xsl:when test="@level=4">
                <ul><ul><ul><li><a>
          <xsl:attribute name="href">
              <xsl:text>#</xsl:text>
              <xsl:value-of select="following::*[@xml:id][1]/@xml:id"/>
          </xsl:attribute>
                    <!--xsl:apply-templates select="."/-->
                    <!--xsl:copy-of select="."/-->
                    <xsl:value-of select="."/>
          </a></li></ul></ul></ul>
            </xsl:when>
        </xsl:choose>
      </xsl:for-each>
    </xsl:template>

    <!--cb:yin><cb:zi>得浪</cb:zi><cb:sg>二合</cb:sg></cb:yin-->
    <xsl:template match="cb:sg"><span class="note"><xsl:apply-templates/></span></xsl:template>

    <!--公式强调角标-->
    <xsl:template match="hi">
        <span class="formula">
            <xsl:if test="@rend">
                <xsl:attribute name="style">
                    <xsl:value-of select="@rend"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </span>
    </xsl:template>


    <!-- <ref target="#PTS.Ja.3.227" type="PTS_hide"> -->
    <!-- <ref target="#PTS.Ja.3.153"> -->
    <!-- <ref cRef="PTS.Ja.1.1"/> -->
    <!-- <ref target="../T31/T31n1585.xml#xpath2(//0041b09)"> TODO-->
    <!-- <ref target="../T31/T31n1585_008.xml#0041b09)"> TODO -->
    <!-- <ref target="#vol:24;page:p900c" type="taisho"> -->
    <!-- 《中阿含經》</title><ref target="#no:26.73" type="taisho">（七三）</ref-->
    <!-- <ref target="#vol:19;page:p570" type="taixu">(ref taixu::vol:19;page:p570)</ref -->
    <xsl:template match="ref">
        <a>
            <xsl:attribute name="href">
               <!--xsl:value-of select="concat($current_sutra, '_p', @n)" /-->
                <xsl:if test="@target">
                  <xsl:value-of select="@target"/>
                </xsl:if>
                <xsl:if test="@cRef">
                  <xsl:value-of select="@cRef"/>
                </xsl:if>
            </xsl:attribute>
            <!--xsl:value-of select="."/-->
            <xsl:choose>
            <xsl:when test="not(text())">
                <sup lang="en">[pts]</sup>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
            </xsl:choose>
        </a>
    </xsl:template>

    <xsl:template match="quote">
      <q>
      <xsl:if test="@source">
        <xsl:attribute name="cite">
          <xsl:value-of select="@source"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
      </q>
    </xsl:template>

    <!-- <term rend="no_nor"> 此标签内的g不规范化-->
    <xsl:template match="term">
        <dfn class="term">
            <xsl:apply-templates/>
        </dfn>
    </xsl:template>

    <!--'sa-x-rj', 'en', 'sa-Sidd', 'zh', 'san-tr', 'sa', 'x-unknown', 'pi', 'zh-x-yy'-->
    <!--sa, pi, x-unknown, x-sa-pi-->
    <xsl:template match="foreign">
        <!--span>
            <xsl:attribute name="lang">
              <xsl:value-of select="@xml:lang"/>
            </xsl:attribute>
        </span-->
        <xsl:choose>
            <xsl:when test="@xml:lang='en'">
                <xsl:text>英&#x20DE;</xsl:text>
            </xsl:when>
            <xsl:when test="@xml:lang='x-sa-pi'">
                <xsl:text>梵&#x20DE;巴&#x20DE;</xsl:text>
            </xsl:when>
            <xsl:when test="@xml:lang='sa'">
                <xsl:text>梵&#x20DE;</xsl:text>
            </xsl:when>
            <xsl:when test="@xml:lang='pi'">
                <xsl:text>巴&#x20DE;</xsl:text>
            </xsl:when>
            <xsl:when test="@xml:lang='x-unknown'">
                <xsl:text>？&#x20DE;</xsl:text>
            </xsl:when>
        </xsl:choose>
                <xsl:apply-templates/>
    </xsl:template>

    <!-- 经录的卷数 -->
    <xsl:template match="cb:jl_juan">
        <span class="jl">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- 经录的标题: TODO 做一个超链接到应该的文件 -->
    <xsl:template match="cb:jl_title|item/title">
        <cite>
            <a>
                <xsl:attribute name="href">
                    <xsl:text>/searchmulu?title=</xsl:text>
                    <xsl:apply-templates/>   <!--TODO 应该去掉这里的注释-->
                </xsl:attribute>
            <xsl:apply-templates/>
            </a>
        </cite>
    </xsl:template>

    <!--敬语-->
    <xsl:template match="Honorific">
        <span class="honorific">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!--人名地名-->
    <!--xsl:template match="persName">
        <span class="persName">
            <xsl:apply-templates/>
        </span>
    </xsl:template-->

    <!--string-split函数: 空格分割后取值witness@id-->
    <xsl:template match="text/text()" name="tokenize">
        <xsl:param name="string" select="."/>
        <xsl:param name="delimiters" select="' '"/>
        <xsl:choose>
            <xsl:when test="not(contains($string, $delimiters))">
                <xsl:value-of select="key('witness_id', substring(normalize-space($string), 2))"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="key('witness_id', substring(normalize-space(substring-before($string, $delimiters)), 2))"/>
                <xsl:call-template name="tokenize">
                    <xsl:with-param name="string" select="substring-after($string, $delimiters)"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!--注音模板, 使用kx.xml作为字典给全文注音-->
    <!--xsl:template match="text/text()" name="zhuyin">
        <xsl:param name="string" select="."/>
        <xsl:param name="num" select="1"/>
                <xsl:variable name="zi" select="substring($string, $num, 1)"/>
                <ruby>
                    <xsl:value-of select="substring($string, $num, 1)"/>
                    <rt>
                        <xsl:value-of select="document('kx.xml')//char[@zi=$zi]"/>
                    </rt>
                </ruby>
            <xsl:if test="substring($string, $num+1, 1)">
                <xsl:call-template name="zhuyin">
                    <xsl:with-param name="string" select="substring($string, $num+1)"/>
                </xsl:call-template>
            </xsl:if>
    </xsl:template-->

    <!--计数循环-->
    <xsl:template name="loop">
        <xsl:param name="Count"/>
        <xsl:if test="$Count&lt;1">
            <xsl:value-of select="'finish'"/>
        </xsl:if>
        <xsl:if test="$Count&gt;=1">
            <xsl:value-of select="$Count"/>
            <xsl:call-template name="loop">
                <xsl:with-param name="Count"><xsl:value-of select="number($Count)-1"/></xsl:with-param>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>

