#!/bin/bash

DATA_URL="http://bllip.cs.brown.edu/download/genia1.0-division-rel1.tar.gz"

SCRIPT_DIR="../../scripts"
STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

if [ ! -e genia1.0-division-rel1.tar.gz ]; then
    wget ${DATA_URL} genia1.0-division-rel1.tar.gz
fi

# This overrides any previous extracted copy
tar xf genia1.0-division-rel1.tar.gz

for SPLIT in train dev test
do
  RAW=genia-dist/division/${SPLIT}.trees
  STRIPPED=${SPLIT}.stripped

  python $STRIP_ROOT --symbol S1 --must_have < $RAW | python $STRIP_ROOT --symbol S --must_have | python $ENSURE_TOP > $STRIPPED
done
