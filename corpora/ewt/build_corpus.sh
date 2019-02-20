#!/bin/bash

RAW="Brown.goldtags.train"
STRIPPED=${RAW}.stripped

SCRIPT_DIR="../../scripts"

STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

# python get_ewt.py

for CATEGORY in answers email newsgroup reviews weblog
do
  for SPLIT in dev test
  do
    STRIPPED=${CATEGORY}.${SPLIT}.stripped
    python $STRIP_FUNCTIONAL < ${CATEGORY}.${SPLIT}.original | python $ENSURE_TOP > $STRIPPED
  done
done
