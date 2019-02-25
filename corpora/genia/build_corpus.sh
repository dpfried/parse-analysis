#!/bin/bash

DATA_URL="http://bllip.cs.brown.edu/download/genia1.0-division-rel1.tar.gz"

SCRIPT_DIR="../../scripts"

TAGGER_DIR="../../taggers"

STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py
PREDICT_TAGS=${SCRIPT_DIR}/predict_tags.py

if [ ! -e genia1.0-division-rel1.tar.gz ]; then
    wget ${DATA_URL} genia1.0-division-rel1.tar.gz
fi

# This overrides any previous extracted copy
tar xf genia1.0-division-rel1.tar.gz

for SPLIT in train dev test
do
  RAW=genia-dist/division/${SPLIT}.trees
  STRIPPED=${SPLIT}.gold.stripped

  python $STRIP_ROOT --symbol S1 --must_have < $RAW | python $STRIP_ROOT --symbol S --must_have | python $ENSURE_TOP > $STRIPPED
done

mkdir tag_predictions 2> /dev/null

python $PREDICT_TAGS \
  --props_file ${TAGGER_DIR}/retrain-wsj-2-21-bidirectional-nodistsim.tagger.props \
  --model_file ${TAGGER_DIR}/retrain-wsj-2-21-bidirectional-nodistsim.tagger  \
  --working_dir tag_predictions \
  --held_out_names train dev test \
  --held_out_gold_files train.gold.stripped dev.gold.stripped test.gold.stripped \
  --held_out_pred_files train.pred.stripped dev.pred.stripped test.pred.stripped \
