#!/bin/bash

SCRIPT_DIR="../../scripts"

TAGGER_DIR="../../taggers"

STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py
PREDICT_TAGS=${SCRIPT_DIR}/predict_tags.py

python get_ewt.py --data_root ../../data/eng_web_tbk/data

SECTIONS=(answers email newsgroup reviews weblog)

SPLIT_NAMES=()
GOLD_FILES=()
PRED_FILES=()


for SECTION in ${SECTIONS[@]}
do
  for SPLIT in dev test
  do
    STRIPPED=${SECTION}.${SPLIT}.gold.stripped
    PRED=${SECTION}.${SPLIT}.pred.stripped

    SPLIT_NAMES+=(${SECTION}.${SPLIT})
    GOLD_FILES+=($STRIPPED)
    PRED_FILES+=($PRED)

    python $ENSURE_TOP < ${SECTION}.${SPLIT}.original | python $STRIP_FUNCTIONAL > $STRIPPED
  done
done

mkdir tag_predictions 2> /dev/null

python $PREDICT_TAGS \
  --props_file ${TAGGER_DIR}/retrain-wsj-2-21-bidirectional-nodistsim.tagger.props \
  --model_file ${TAGGER_DIR}/retrain-wsj-2-21-bidirectional-nodistsim.tagger  \
  --working_dir tag_predictions \
  --held_out_names ${SPLIT_NAMES[@]} \
  --held_out_gold_files ${GOLD_FILES[@]} \
  --held_out_pred_files ${PRED_FILES[@]} \

  #--model_file ${TAGGER_DIR}/retrain-wsj-2-21-left3words-nodistsim.tagger \
