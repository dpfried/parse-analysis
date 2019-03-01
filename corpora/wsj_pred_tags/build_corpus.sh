#!/bin/bash

SCRIPT_DIR="../../scripts"

ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
PREDICT_TAGS=${SCRIPT_DIR}/predict_tags.py

python get_wsj.py --data_root ../treebank_3/parsed/mrg/wsj

TRAIN="train_02-21.gold.original"
DEV="dev_22.gold.original"
TEST="test_23.gold.original"

TAGGER_DIR="../../taggers"

python $STRIP_FUNCTIONAL < $TRAIN | python $ENSURE_TOP > train.gold.stripped
python $STRIP_FUNCTIONAL < $DEV | python $ENSURE_TOP > dev.gold.stripped
python $STRIP_FUNCTIONAL < $TEST | python $ENSURE_TOP > test.gold.stripped

# python $PREDICT_TAGS \
#   --props_file ${TAGGER_DIR}/wsj-0-18-bidirectional-nodistsim.tagger.props \
#   --model_file ${TAGGER_DIR}/retrain-wsj-2-21-bidirectional-nodistsim.tagger \
#   --working_dir tag_predictions \
#   --train_gold_file train.gold.stripped \
#   --held_out_names dev test \
#   --held_out_gold_files dev.gold.stripped test.gold.stripped \
#   --held_out_pred_files dev.pred.stripped test.pred.stripped \
#   --train_pred_file train.pred.stripped \
#   --jackknife \
#   --jackknife_num_splits 10 \
#   --train_models \
