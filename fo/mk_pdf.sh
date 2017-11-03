#!/bin/bash

# 使用说明: 修改fop.xconf中字体文件所在位置(directory标签内容).然后执行
# $ sh mk_pdf.sh tei_format_xml_file_name
# 即可在当前目录生成同名pdf文件. 使用fop版本2.1

# fop -c fop.xconf -xml ../../xml/T01/T01n0001_001.xml  -xsl tei2fo.xsl -pdf name.pdf
filename=${1##*/}
fop -c fop.xconf -xml $1 -xsl tei2fo.xsl -pdf "${filename%.*}.pdf"
