#!/bin/bash

RAW="Brown.mrg"
STRIPPED=all.stripped

SCRIPT_DIR="../../scripts"

TAGGER_DIR="../../taggers"

STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py
PREDICT_TAGS=${SCRIPT_DIR}/predict_tags.py

python $STRIP_ROOT --symbol '' < $RAW | python $ENSURE_TOP | python $STRIP_FUNCTIONAL >$STRIPPED

python partition_brown.py --split 'train' <$STRIPPED >train.gold.stripped
python partition_brown.py --split 'test' <$STRIPPED >test.gold.stripped
python partition_brown.py --split 'test40' <$STRIPPED >test40.gold.stripped

SECTIONS=(cf cg ck cl cm cn cp cr)
GOLD_FILES=()
PRED_FILES=()

for SECTION in ${SECTIONS[@]}
do
  GOLD_FILES+=(${SECTION}.gold.stripped)
  PRED_FILES+=(${SECTION}.pred.stripped)

  python split_brown_by_section.py --section $SECTION <$STRIPPED >${SECTION}.gold.stripped
done

mkdir tag_predictions

python $PREDICT_TAGS \
  --props_file ${TAGGER_DIR}/retrain-wsj-2-21-bidirectional-nodistsim.tagger.props \
  --model_file ${TAGGER_DIR}/retrain-wsj-2-21-bidirectional-nodistsim.tagger  \
  --working_dir tag_predictions \
  --held_out_names ${SECTIONS[@]} \
  --held_out_gold_files ${GOLD_FILES[@]} \
  --held_out_pred_files ${PRED_FILES[@]} \

  #--model_file ${TAGGER_DIR}/retrain-wsj-2-21-left3words-nodistsim.tagger \
