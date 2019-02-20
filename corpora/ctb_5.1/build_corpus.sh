#!/bin/bash

TRAIN="train.gold.original"
DEV="dev.gold.original"
TEST="test.gold.original"

SCRIPT_DIR="../../scripts"
REMOVE_TRACES=${SCRIPT_DIR}/remove_traces.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

# python process_ctb.py --ctb ${HOME}/data/ctb_5.1/

for SPLIT in train dev test
do
  STRIPPED=${SPLIT}.gold.stripped
  rm $STRIPPED
  python $REMOVE_TRACES < ${SPLIT}.gold.original | python $STRIP_FUNCTIONAL | python $ENSURE_TOP > $STRIPPED
done

# this should produce {train,dev,test}.pred.stripped
# cd jackknife
# python jackknnife.py
# cd ..
