#!/bin/bash

SCRIPT_DIR="../../scripts"
STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

for SPLIT in train dev test
do
  RAW=${SPLIT}.trees
  STRIPPED=${SPLIT}.stripped
  PROCESSED=${SPLIT}.processed

  python $STRIP_ROOT --symbol S1 --must_have < $RAW | python $STRIP_ROOT --symbol S --must_have | python $ENSURE_TOP > $STRIPPED  
done
