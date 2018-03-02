<?xml version="1.0" encoding="utf8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">
    <!--xpath-default-namespace="http://www.tei-c.org/ns/1.0"-->
    <xsl:output method="html" encoding="utf8" doctype-system="about:legacy-compat" indent="yes"/>
    <xsl:variable name="title" select="/TEI/teiHeader/fileDesc/titleStmt/title"/>
    <!--将丁福宝词典转成html格式, 其实是python的字典, 其中回车替换成了_
    $ xsltproc dfb.xsl dingfubao.ddbc.tei.p5.xml > dfb.json
    with open('dfb.json') as fd: 
    	data = fd.read()
    	dd = eval(data)
	print(json.dumps(dd, ensure_ascii=False).replace('_', '\\n'))
         -->


    <xsl:template match="/">
        <html>
            <xsl:attribute name="lang">
                <xsl:value-of select="/TEI/@xml:lang"/>
            </xsl:attribute>
        <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no"/>
        <meta name="description" content="印刷品般的经典阅读"/>
        <meta name="keywords" content="漢字標準格式, 中文, 排版, 排版規範, 日文, 字體排印, 文字設計, CLReq, CSS, Sass, typography"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>
        <!--link rel="stylesheet" href="http://han-css.herokuapp.com/style.css"/-->
        <link rel="stylesheet" href="/static/jquery.webui-popover.min.css"/>
        <link rel="stylesheet" href="/static/tei.css"/>
        <!--link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Han/3.2.7/han.min.css"/-->
        <title>
            <!--xsl:value-of select="concat($current_sutra, ' ', $title)"/-->
            <xsl:value-of select="$title"/>
        </title>
        <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
        <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script src="/static/jquery.webui-popover.min.js"></script>
        <!--script src="https://cdnjs.cloudflare.com/ajax/libs/Han/3.2.7/han.min.js"></script-->
        <!--[if lt IE9]> 
        <script src="http://cdn.staticfile.org/html5shiv/r29/html5.min.js"></script>
        <![endif]-->
        <script src="/static/my.js"></script>
        
        </head>
        <body>
            <div id="topAnchor"/>
            <a href="#topAnchor" style="position:fixed;right:0;bottom:0" rel="bookmark">&#x21c8;</a>  <!--回到顶部-->
            <a href="#bottomAnchor" style="position:fixed;right:0;top:70" rel="bookmark">&#x21ca;</a> <!--回到底部-->
            <h1 class="title">
                <xsl:value-of select="$title"/>
            </h1>
            <br/>
            <br/>
            <xsl:apply-templates select="/TEI/teiHeader/fileDesc/sourceDesc"/>
            <br/>
            <xsl:apply-templates/>
            <div id="bottomAnchor"/>
        </body>

        </html>
    </xsl:template>


    <xsl:key name="form_id" match="form" use="text()"/>

    <xsl:template match="teiHeader"/>
    <xsl:template match="head"/>

    <xsl:template match="p">
        <p>
            <xsl:attribute name="lang">
                <xsl:value-of select="@xml:lang"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <!--清除文档中无用空格-->
    <xsl:template match="text()|@*">
      <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>

    <!--处理词典-->

    <!--xsl:template match="sense">
        <li>
            <xsl:apply-templates/>
        </li>
    </xsl:template-->

    <!--交互参照 -->
    <xsl:template match="xr">
        <xsl:text>&#128409; </xsl:text>
        <a>
            <xsl:attribute name="href">
                <xsl:text>#</xsl:text>
                <xsl:value-of select="text()"/>
                <!--xsl:value-of select="key('form_id', text())"/-->
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>


    <xsl:template match="usg">
        <xsl:text>  [</xsl:text>
            <xsl:apply-templates/>
        <xsl:text>]</xsl:text>
    </xsl:template>

    <xsl:template match="entry">
        <dl>
            <xsl:attribute name="id">
                <!--xsl:value-of select="generate-id()"/-->
                <xsl:value-of select="form"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </dl>
    </xsl:template>

    <xsl:template match="form"><dt style="display:inline-block;"><xsl:apply-templates/></dt></xsl:template>
    <xsl:template match="def"><dd style="text-indent: 2em;"><xsl:apply-templates/></dd></xsl:template>

  <!--entry>
    <form>戒波羅蜜教主</form>
    <sense>
      <usg type="dom">雜語</usg>
      <def>說梵網菩薩戒之盧舍那佛也。是為坐千葉蓮花臺之報身佛。梵網經下曰：「我今盧舍那，方坐蓮花臺周匝千花上。」</def>
    </sense>
  </entry-->


</xsl:stylesheet>

