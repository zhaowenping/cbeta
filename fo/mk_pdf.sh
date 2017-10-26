# 修改fop.xconf文件中directory标签内容为字体所在目录，修改下面脚本，即可生成pdf文件
fop -c fop.xconf -xml ../../xml/T01/T01n0001_001.xml  -xsl tei2fo.xsl -pdf name.pdf
