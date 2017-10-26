<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
      xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
      xmlns:fo="http://www.w3.org/1999/XSL/Format">
  <xsl:output method="xml" indent="yes"/>


    <!--当前经集的名字, 形如: T20n1167 -->
    <xsl:variable name="current_sutra" select="/TEI[1]/@xml:id"/>
    <xsl:variable name="current_han" select="substring(substring-before($current_sutra, 'n'), 2)"/>  <!--XXX T20-->
    <xsl:variable name="current_ce" select="substring-after($current_sutra, 'n')"/> <!---1167-->
    <xsl:variable name="title" select="substring-after(substring-after(/TEI/teiHeader/fileDesc/titleStmt/title, 'No. '), ' ')"/>
    <!--当前文件的卷数, 形如: 001; 目前只能靠猜了-->
    <!--xsl:variable name="juan" select="/TEI[1]/text/body//cb:juan[1]/@n|/TEI/text/body//milestone[@unit='juan']/@n|/TEI/text/body//cb:mulu[@type='卷']/@n"/-->
    <xsl:variable name="juan" select="/TEI/text/body//milestone[@unit='juan']/@n"/>

  <xsl:template match="/">
    <fo:root>
      <fo:layout-master-set>
        <!--fo:simple-page-master master-name="A4-portrait"
              page-height="29.7cm" page-width="21.0cm" margin="2cm">
          <fo:region-body/>
        </fo:simple-page-master-->

         <fo:simple-page-master master-name="A4-portrait"
                  page-height="29.7cm" 
                  page-width="21cm"
                  margin-top="1cm" 
                  margin-bottom="2cm" 
                  margin-left="2.5cm" 
                  margin-right="2.5cm">
            <fo:region-body margin-top="3cm"/>
            <fo:region-before extent="3cm"/>
            <fo:region-after extent="1.5cm"/>
        </fo:simple-page-master>

      </fo:layout-master-set>
      <fo:page-sequence master-reference="A4-portrait">
        <fo:flow flow-name="xsl-region-body">
          <fo:block font-family="PingFang SC"
                line-height="15pt"
                space-after.optimum="3pt"
                font-weight="bold"
                font-size="1.8em"
                margin-bottom="0.8em"
                text-align="center">
                <xsl:value-of select="concat($current_sutra, ' ', $title)"/>
          </fo:block>

          <fo:block font-size="12pt" 
                font-family="SimSun" 
                line-height="15pt"
                space-after.optimum="3pt"
                color="#336633"
                text-align="right">
                <xsl:value-of select="/TEI/teiHeader/fileDesc/titleStmt/author"/>
          </fo:block>

<xsl:apply-templates/>


        </fo:flow>
      </fo:page-sequence>
    </fo:root>
  </xsl:template>

    <xsl:template match="teiHeader"/>

    <!--不显示back部分-->
    <xsl:template match="text/back">
    </xsl:template>

    <!--不显示目录-->
    <!--xsl:template match="cb:mulu">
    </xsl:template-->

    <xsl:template match="lg">
          <fo:block font-size="12pt" 
                font-family="SimSun" 
                line-height="15pt"
                space-after.optimum="3pt"
                margin-bottom="1em"
                margin-top="0"
                margin-left="4em"
                text-indent="0"
                color="#10AA10"
                text-align="justify">
          <xsl:apply-templates/>
          </fo:block>
    </xsl:template>

    <xsl:template match="p">
          <!--fo:block line-height="162%"
                    text-indent="2em"
                    white-space="normal"
                    font-size="1em"
                    font-weight="normal"
                    letter-spacing="0.12em"
                font-family="PingFang SC" 
                space-after.optimum="3pt"
                text-align="justify"-->
          <fo:block font-family="SimSun"
                line-height="162%"
                    text-indent="2em"
                    white-space="normal"
                space-after.optimum="3pt"
                font-weight="bold"
                font-size="1em"
                    letter-spacing="0em"
                margin-bottom="0.8em"
                text-align="justify">
          <xsl:apply-templates/>
          </fo:block>
    </xsl:template>

    <xsl:template match="l">
          <fo:block line-height="162%"
                    white-space="normal"
                    font-size="1em"
                    font-weight="normal"
                    letter-spacing="0.12em"
                    font-family="SimSun" 
                 margin-left="1em"
                 color="#10AA10"
                text-align="justify">
          <xsl:apply-templates/>
          </fo:block>
    </xsl:template>

   <xsl:template match="text()|@*">
       <xsl:value-of select="normalize-space(.)"/>
   </xsl:template>


</xsl:stylesheet>
