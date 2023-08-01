#!/bin/bash
./html_to_docbook.py
if [ $? != 0 ]; then
  echo "Could not run html_to_docbook.py";
  exit
fi
echo "Created ugly.xml..."

xmllint --schema docbook.xsd --noout ugly.xml
if [ $? != 0 ]; then
  echo "ugly.xml does not validate";
  exit
fi
echo "Validated ugly.xml..."

xmllint --format --output dockbook.xml ugly.xml
if [ $? != 0 ]; then
  echo "Could not format ugly.xml into docbook.xml";
  exit
fi
echo "Prettified ugly.xml to docbook.xml"