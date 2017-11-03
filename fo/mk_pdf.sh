#!/bin/bash

# fop -c fop.xconf -xml ../../xml/T01/T01n0001_001.xml  -xsl tei2fo.xsl -pdf name.pdf
filename=${1##*/}
fop -c fop.xconf -xml $1 -xsl tei2fo.xsl -pdf "${filename%.*}.pdf"
