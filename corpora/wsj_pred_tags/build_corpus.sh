#!/bin/bash

TRAIN="02-21.10way.clean"
DEV="22.auto.clean"
TEST="23.auto.clean"

DATA_URL="https://raw.githubusercontent.com/jhcross/span-parser/d6ca8e3f2a5b7eda8d06dce85663456f8a92efbc/data/"

SCRIPT_DIR="../../scripts"

ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

# get cross and huang cleaned version of PTB, which strips functional annotations and has predicted tags

for fname in $TRAIN $DEV $TEST
do
  rm $fname 2> /dev/null
done

wget ${DATA_URL}${TRAIN}
wget ${DATA_URL}${DEV}
wget ${DATA_URL}${TEST}

python $ENSURE_TOP < $TRAIN > train.stripped
python $ENSURE_TOP < $DEV > dev.stripped
python $ENSURE_TOP < $TEST > test.stripped
