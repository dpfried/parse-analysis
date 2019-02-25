#!/bin/bash

TRAIN="train.gold.original"
DEV="dev.gold.original"
TEST="test.gold.original"

SCRIPT_DIR="../../scripts"
REMOVE_TRACES=${SCRIPT_DIR}/remove_traces.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py
PREDICT_TAGS=${SCRIPT_DIR}/predict_tags.py

python process_ctb.py --ctb ${HOME}/data/ctb_5.1/

for SPLIT in train dev test
do
  STRIPPED=${SPLIT}.gold.stripped
  rm $STRIPPED
  python $REMOVE_TRACES < ${SPLIT}.gold.original | python $STRIP_FUNCTIONAL | python $ENSURE_TOP > $STRIPPED
done

# this should produce {train,dev,test}.pred.stripped

python $PREDICT_TAGS \
  --props_file jackknife/train-chinese-nodistsim.tagger.props \
  --working_dir jackknife \
  --jackknife \
  --jackknife_num_splits 10 \
  --train_gold_file train.gold.stripped \
  --train_pred_file train.pred.stripped \
  --held_out_names dev test \
  --held_out_gold_files dev.gold.stripped test.gold.stripped \
  --held_out_pred_files dev.pred.stripped test.pred.stripped \
  # --train_models
