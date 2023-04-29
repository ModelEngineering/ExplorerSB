#!/bin/bash
# Construct the archive. Separate archive files are created for each runid
cd data
for d in 6*
do
  zip $d.zip $d/*.ant $d/*.csv $d/*.xml $d/*.sedml $d/*.xml $d/*.cellml $d/*.json
  zip -d $d.zip "*/manifest.xml"
done
