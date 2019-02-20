#!/bin/bash

RAW="Brown.mrg"
STRIPPED=all.stripped

SCRIPT_DIR="../../scripts"

STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

python $STRIP_ROOT --symbol '' < $RAW | python $ENSURE_TOP | python $STRIP_FUNCTIONAL | python $ENSURE_TOP >$STRIPPED

python partition_brown.py --split 'train' <$STRIPPED >train.stripped
python partition_brown.py --split 'test' <$STRIPPED >test.stripped
python partition_brown.py --split 'test40' <$STRIPPED >test40.stripped
