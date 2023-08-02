#!/bin/bash



./extract_main.py
if [ $? != 0 ]; then
  echo "Could not run html_to_docbook.py";
  exit
fi
echo "Created temporary.html..."
saxon -xsl:html_docbook.xsl -s:temporary.html -o:ugly.xml
if [ $? != 0 ]; then
  echo "Could not transform to ugly.xml";
  exit
fi
echo "Created ugly.xml..."
xmllint --format --output docbook.xml ugly.xml
if [ $? != 0 ]; then
  echo "Could not format ugly.xml into docbook.xml";
  exit
fi
echo "Prettified ugly.xml to docbook.xml"