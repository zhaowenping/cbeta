<?xml version="1.0" encoding="utf8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cb="http://www.cbeta.org/ns/1.0">
    <xsl:output method="html" encoding="utf8" doctype-system="about:legacy-compat" indent="yes"/>
    <!--xpath-default-namespace="http://www.tei-c.org/ns/1.0"-->

    <xsl:template match="/">
        <html lang="zh_TW">
        <head>
         <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0"/>
         <!--link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/-->
         <link rel="stylesheet" type="text/css" href="/stylesheet/tei.css"/>
         <title>
            <xsl:value-of select="//teiHeader//title"/>
        </title>

         <script> </script>
        </head>

        <body>

    <!--侧边栏目录-->
        <!--nav>
        <ul>
            <xsl:for-each select="//cb:mulu">
        <xsl:choose>
            <xsl:when test="@level=1">
                <li><a>
          <xsl:attribute name="href">
              <xsl:text>#</xsl:text>
            <xsl:value-of select="p[@xml:id]"/>
          </xsl:attribute>
                        <xsl:value-of select="."/></a></li>
            </xsl:when>
            <xsl:when test="@level=2">
                <ul><li><a href="#"><xsl:value-of select="."/></a></li></ul>
            </xsl:when>
            <xsl:when test="@level=3">
                <ul><ul><li><a href="#"><xsl:value-of select="."/></a></li></ul></ul>
            </xsl:when>
        </xsl:choose>
            </xsl:for-each>
        </ul>
        </nav-->

            <br/>
            <xsl:apply-templates/>
        </body>
        </html>
    </xsl:template>

    <!--处理整体结构: TEI\teiHeader\app-->

    <xsl:template match="TEI">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="teiHeader"/>

    <!--测试没通过-->
    <xsl:template match="pb">
      <!--xsl:call-template name="makeAnchor"/-->
      <!--p style="page-break-before: always"> </p-->
        <span>
          <xsl:attribute name="id">
            <xsl:value-of select="@xml:id"/>
          </xsl:attribute>
          <xsl:comment>anchor</xsl:comment>
        </span>
    </xsl:template>

 <xsl:template match="app">
    <xsl:variable name="identifier">
      <xsl:text>App</xsl:text>
      <xsl:choose>
    <xsl:when test="@id">
      <xsl:value-of select="@id"/>
    </xsl:when>
    <xsl:when test="@n">
      <xsl:value-of select="@n"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:number count="app" level="any"/>
    </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <a class="notelink" href="#{$identifier}">
   <span class="lem"> <xsl:value-of select="lem"/> </span>
      <!--sup>
        <xsl:call-template name="appN"/>
      </sup-->
    </a>
  </xsl:template>

  <!--处理表格table-->
  <!--TODO: table rend="border:0"-->
    <xsl:template match="table">
        <table class="table">
            <xsl:apply-templates/>
        </table>
    </xsl:template>
  <!--处理表格row-->
    <xsl:template match="row">
        <tr>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>
  <!--处理表格cell-->
    <xsl:template match="cell">
        <td>
            <xsl:if test="@cols">
            <xsl:attribute name="colspan">
                <xsl:value-of select="@cols"/>
            </xsl:attribute>
            </xsl:if>
            <xsl:if test="@rows">
            <xsl:attribute name="rowspan">
                <xsl:value-of select="@rows"/>
            </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </td>
    </xsl:template>

    <!--处理所有的颂-->
<!-- rend="margin-left:1em;text-indent:-1em" -->
    <xsl:template match="lg">
        <xsl:choose>
            <xsl:when test="@rend">
                <div class="lg">
                    <xsl:attribute name="style">
                    <xsl:text>text-indent:-1em;</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </div>
            </xsl:when>
            <xsl:otherwise>
                <div class="lg">
                    <xsl:apply-templates/>
                </div>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="lg/lb">
        <br/>
        <!--xsl:text disable-output-escaping="yes">&lt;br&gt;</xsl:text-->
    </xsl:template>

    <xsl:template match="lg/l">
       <span>
         <xsl:attribute name="class">
           <xsl:choose>
             <xsl:when test="@rend='Alignr'">
               <xsl:text>right</xsl:text>
             </xsl:when>
             <xsl:when test="@rend='Alignc'">
               <xsl:text>center</xsl:text>
             </xsl:when>
             <xsl:when test="starts-with(@rend,'indent(')">
               <xsl:text>indent</xsl:text>
               <xsl:value-of select="concat(substring-before(substring-after(@rend,'('),')'),'em')" />
             </xsl:when>
             <xsl:when test="@rend='indent'">
               <xsl:text>indent1</xsl:text>
             </xsl:when>
             <xsl:otherwise>
               <xsl:text>l</xsl:text>
             </xsl:otherwise>
           </xsl:choose>
         </xsl:attribute>
         <xsl:apply-templates/>
       </span>&#12288;<!--IDEOGRAPHIC SPACE-->
    </xsl:template>

  <!--清除文档中无用空格-->
  <xsl:template match="text()|@*">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:template>

   <!--处理图片-->
  <!--xsl:template match="figure">
    <img>
      <xsl:attribute name="src">
          <xsl:value-of select="graphic[@url]"/>
      </xsl:attribute>
    </img>
    <figure>
      <xsl:apply-templates/>
    </figure>
  </xsl:template-->
  <xsl:template match="graphic">
    <img>
      <xsl:attribute name="src">
          <xsl:text>/static</xsl:text>
          <xsl:value-of select="substring(@url, 3)"/>
      </xsl:attribute>
    </img>
  </xsl:template>

    <!--处理段落-->
  <xsl:template match="p">
    <p class="p">
      <xsl:if test="@id">
          <xsl:attribute name="id">      
            <xsl:value-of select="@xml:id"/>
          </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <!--xsl:template match="p">
    <xsl:variable name="wrapperElement">
      <xsl:choose>
        <xsl:when test="specList|quote|moduleSpec|list|eg|teix:egXML|table|specGrp|specGrpRef|q[@rend='display']|figure">
          <xsl:text>div</xsl:text>
        </xsl:when>
        <xsl:when test="parent::p">
          <xsl:text>div</xsl:text>
        </xsl:when>
        <xsl:when test="parent::remarks">
          <xsl:text>div</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text>p</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:element name="{$wrapperElement}">
      <xsl:call-template name="rendToClass">
    <xsl:with-param name="default">
      <xsl:if test="$wrapperElement='div'">p</xsl:if>
    </xsl:with-param>
      </xsl:call-template>

      <xsl:choose>
    <xsl:when test="@id">
      <xsl:call-template name="makeAnchor">
        <xsl:with-param name="name">
          <xsl:value-of select="@id"/>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:when>
    <xsl:when test="$generateParagraphIDs='true'">
      <xsl:call-template name="makeAnchor">
        <xsl:with-param name="name">
          <xsl:value-of select="generate-id()"/>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:when>
      </xsl:choose>
      <xsl:if test="$numberParagraphs='true'">
        <xsl:number/>
        <xsl:text> </xsl:text>
      </xsl:if>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template-->

<!--处理note TODO -->
  <xsl:template match="note[@place='inline']">
      <span style="color:#A9A9A9">(<xsl:apply-templates/>)</span>
  </xsl:template>

  <xsl:template match="note">
    <xsl:if test="@type='inline'">
        (<xsl:apply-templates/>)
    </xsl:if>
    <xsl:variable name="identifier">
      <xsl:text>Note</xsl:text>
      <!--xsl:call-template name="noteID"/-->
    </xsl:variable>
    <xsl:choose>
      <xsl:when test="ancestor::bibl"> (<xsl:apply-templates/>) </xsl:when>
      <!--xsl:when test="@place='inline'">
    <xsl:call-template name="makeAnchor">
      <xsl:with-param name="name" select="$identifier"/>
    </xsl:call-template>
        <xsl:text> (</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>)</xsl:text>
      </xsl:when-->
      <xsl:when test="@place='display'">
    <!--xsl:call-template name="makeAnchor">
      <xsl:with-param name="name" select="$identifier"/>
    </xsl:call-template-->
        <blockquote>
      <xsl:choose>
        <xsl:when test="@rend">
          <xsl:attribute name="class">      
        <xsl:value-of select="@rend"/>
          </xsl:attribute>
        </xsl:when>
        <xsl:when test="@rendition">
          <!--xsl:call-template name="applyRendition"/-->
        </xsl:when>
        <xsl:otherwise>
          <xsl:attribute name="class">
          <xsl:text>note</xsl:text>
          </xsl:attribute>
        </xsl:otherwise>
      </xsl:choose>
      <p> <xsl:apply-templates/> </p>
        </blockquote>
      </xsl:when>
      <xsl:when test="@place='foot' or @place='end'">
    <!--xsl:call-template name="makeAnchor">
      <xsl:with-param name="name" select="concat($identifier,'_return')"/>
    </xsl:call-template-->
        <a class="notelink" title="Go to note" href="#{$identifier}">
            <sup> <!--xsl:call-template name="noteN"/--> noteN </sup>
        </a>
      </xsl:when>
      <xsl:otherwise>
    <!--xsl:call-template name="makeAnchor">
      <xsl:with-param name="name" select="$identifier"/>
    </xsl:call-template>
        <xsl:text> [</xsl:text>
        <xsl:call-template name="i18n">
          <xsl:with-param name="word">Note</xsl:with-param>
        </xsl:call-template-->
        <xsl:text>: </xsl:text>
        <xsl:apply-templates/>
        <xsl:text>]</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="note[@type='action']">
    <div class="right"><b>Action <xsl:number count="note[@type='action']" level="any"/>
         </b>: <i><xsl:apply-templates/></i></div>
  </xsl:template>
<!--处理note TODO end -->

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
      <xsl:text> </xsl:text>
    </span>
  </xsl:template>


  <!--xsl:template match="juan">
          <xsl:apply-templates/>
  </xsl:template-->

  <xsl:template match="t">
      <xsl:if test="@lang='chi'">
          <xsl:apply-templates/>
      </xsl:if>
      <xsl:if test="@lang='san-sd'">
          (<xsl:apply-templates/>)
      </xsl:if>
  </xsl:template>

  <!--处理异体字-->
  <xsl:template match="g">
      <!--span class="gaiji"><xsl:value-of select="."/></span-->
      <xsl:variable name="Ref" select="substring(@ref, 2)"/>
      <span class="gaiji">
 <!--localName>normalized form</localName>
 <localName>Character in the Siddham font</localName>   xml:id="SD-E2F6"
 <localName>big5</localName>                            xml:id="SD-E2F6"
 <localName>composition</localName> 组字式              xml:id="CB00178"
 <localName>rjchar</localName>                          xml:id="RJ-CBD3"
 <localName>Romanized form in CBETA transcription</localName>
 <localName>Romanized form in Unicode transcription</localName-->
    <xsl:choose>
        <xsl:when test="starts-with($Ref, 'SD')">
            <ruby><img>
                <xsl:attribute name="src">
                    <xsl:text>/static/sd-gif/</xsl:text>
                    <xsl:value-of select="substring($Ref, 4, 2)"/>
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="$Ref"/>
                    <xsl:text>.gif</xsl:text>
                </xsl:attribute>
                </img>
            <!--xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='Character in the Siddham font']/value"/>
            <xsl:value-of select="."/-->
                <rt>
    <xsl:choose>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in Unicode transcription']/value">
            (<xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in Unicode transcription']/value"/>)
        </xsl:when>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in CBETA transcription']/value">
            (<xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in CBETA transcription']/value"/>)
        </xsl:when>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='Character in the Siddham font']/value">
            <xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='Character in the Siddham font']/value"/>
        </xsl:when>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='big5']/value">
            <xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='big5']/value"/>
        </xsl:when>
    </xsl:choose>
            </rt>
        </ruby>
        </xsl:when>
        <!--蘭札字-->
        <xsl:when test="starts-with($Ref, 'RJ')">
            <ruby>
                <img>
                <xsl:attribute name="src">
                    <xsl:text>/static/rj-gif/</xsl:text>
                    <xsl:value-of select="substring($Ref, 4, 2)"/>
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="$Ref"/>
                    <xsl:text>.gif</xsl:text>
                </xsl:attribute>
                </img>
            <!--xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='rjchar']/value"/-->
                <rt>
    <xsl:choose>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in Unicode transcription']/value">
            (<xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in Unicode transcription']/value"/>)
        </xsl:when>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in CBETA transcription']/value">
            (<xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='Romanized form in CBETA transcription']/value"/>)
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
                </rt>
            </ruby>
        </xsl:when>

        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='normalized form']/value">
            <xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='normalized form']/value"/>
        </xsl:when>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/mapping[@type='unicode']">
            <xsl:value-of select="."/>
        </xsl:when>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='composition']/value">
            <xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='composition']/value"/>
        </xsl:when>
        <xsl:when test="/TEI//char[@xml:id=$Ref]/charProp[localName='rjchar']/value">
            <xsl:value-of select="/TEI//char[@xml:id=$Ref]/charProp[localName='rjchar']/value"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="."/>
        </xsl:otherwise>
    </xsl:choose>
    </span> 
  </xsl:template>

  <xsl:template match="gaiji">
    <xsl:choose>
       <!--xsl:when test="starts-with(@cb,'SD')"><font face="siddam"><xsl:value-of select="@big5"/></font></xsl:when-->
       <xsl:when test="starts-with(@cb,'SD')"><font face="siddam"><xsl:value-of select="@udia"/></font></xsl:when>
         <!-- 若有通用字則以藍色顯示 -->
     <xsl:when test="@nor!=''">
       <font color="blue"><xsl:value-of select="@nor"/></font>
     </xsl:when>
       <!--若unicode標志為0-->
     <xsl:when test="@uniflag='0'">
         <!--span class="nor" title="xxoo" color="blue"--><font color="blue"><xsl:value-of select="@des"/></font><!--/span-->
     </xsl:when>
         <!-- 若有 Unicode 則以 Unicode 顯示 -->
     <xsl:when test="@uni!=''">
         <!--xsl:text disable-output-escaping="yes">&amp;</xsl:text>#x<xsl:value-of select="@uni"/>;</xsl:when-->
   <font color="#00d7ff">
           <xsl:value-of select="@uni"/>
   </font>
         </xsl:when>
         <!-- 組字式 -->
         <xsl:when test="@des!=''"><xsl:value-of select="@des"/></xsl:when>
         <xsl:otherwise><xsl:value-of select="@cb"/></xsl:otherwise>
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
    <h2>
      <xsl:apply-templates/>
    </h2>
  </xsl:template>

  <!--xsl:template match="title">
      <h1 class="title"><xsl:value-of select="."/></h1>
    <br/>
  </xsl:template-->

<!--标题-->
  <xsl:template match="cb:jhead">
  <h1 class="title">
    <xsl:apply-templates/>
  </h1>
    <br/>
  </xsl:template>


   <xsl:template match="byline">
     <div class="byline">
       <xsl:apply-templates/>
     </div>
   </xsl:template>

   <xsl:template match="text">
     <article class="byline">
       <xsl:apply-templates/>
     </article>
   </xsl:template>

   <xsl:template match="text/body">
     <section class="byline">
       <xsl:apply-templates/>
     </section>
   </xsl:template>

   <xsl:template match="text/back">
       <!--hr/>
     <footer class="byline">
       <xsl:apply-templates/>
     </footer-->
   </xsl:template>

   <!--处理列表-->
   <xsl:template match="list">
       <ul>
       <xsl:apply-templates/>
       </ul>
   </xsl:template>

   <xsl:template match="list/item">
       <li>
       <xsl:apply-templates/>
       </li>
   </xsl:template>

<!--处理空缺-->
  <xsl:template match="unclear">
    <span class="unclear">
      <xsl:if test="@xml:id">
        <xsl:attribute name="id">
            <xsl:value-of select="@xml:id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
      &#65533; 
    </span>
  </xsl:template>

  <!--TODO-->
  <!--xsl:template match="anchor">
  </xsl:template-->

<!--处理div评论-->
  <xsl:template match="cb:div[@type='commentary']">
    <div class="commentary">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

</xsl:stylesheet>

