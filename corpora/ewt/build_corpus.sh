#!/bin/bash

SCRIPT_DIR="../../scripts"

STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

python get_ewt.py

for CATEGORY in answers email newsgroup reviews weblog
do
  for SPLIT in dev test
  do
    STRIPPED=${CATEGORY}.${SPLIT}.stripped
    python $ENSURE_TOP < ${CATEGORY}.${SPLIT}.original | python $STRIP_FUNCTIONAL > $STRIPPED
  done
done
