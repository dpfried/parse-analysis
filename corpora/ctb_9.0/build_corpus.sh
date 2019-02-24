#!/bin/bash

TRAIN="train.gold.original"
DEV="dev.gold.original"
TEST="test.gold.original"
OTHERS="others.gold.original"

SCRIPT_DIR="../../scripts"

REMOVE_TRACES=${SCRIPT_DIR}/remove_traces.py
FILTER_BAD=${SCRIPT_DIR}/filter_bad_trees.py
GET_DICTIONARY=${SCRIPT_DIR}/get_dictionary.py
GET_ORACLE=${SCRIPT_DIR}/get_oracle.py
GET_ORACLE_GEN=${SCRIPT_DIR}/get_oracle_gen.py
NORMALIZE_CHINESE=${SCRIPT_DIR}/normalize_chinese_punct.py
NORMALIZE_UNICODE=${SCRIPT_DIR}/normalize_unicode.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py

python get_ctb_9.py

for SPLIT in train dev test
do
  python $REMOVE_TRACES < ${SPLIT}.gold.original \
    | python $NORMALIZE_CHINESE \
    | python $STRIP_FUNCTIONAL \
    | python $ENSURE_TOP \
    > ${SPLIT}.gold.stripped
done

for SPLIT in newswire broadcast_news broadcast_conversations weblogs discussion_forums chat_messages conversational_speech
do
  python $FILTER_BAD < ${SPLIT}.gold.original \
    | python $REMOVE_TRACES \
    | python $NORMALIZE_CHINESE \
    | python $STRIP_FUNCTIONAL --dedup_punct_symbols PU \
    | python $ENSURE_TOP \
    > ${SPLIT}.gold.stripped
done

python pred_tags_ctb_9.py --splits dev test newswire broadcast_news broadcast_conversations weblogs discussion_forums chat_messages conversational_speech
