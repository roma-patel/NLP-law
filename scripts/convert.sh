#!/bin/bash
source /home1/r/romap/crf/crf_task/bin/activate
while read p
do
   inputf="/nlp/data/romap/law/data/district_cases/2_circuit/2010/pdf/"
   inputf="$inputf$p.pdf"
   outputf="/nlp/data/romap/law/data/district_cases/2_circuit/2010/text/"
   outputf="$outputf$p.txt"
   pdf2txt.py -o $outputf $inputf
done < /nlp/data/romap/law/data/district_cases/2_circuit/2010/pdf_names.txt
