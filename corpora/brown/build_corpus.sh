#!/bin/bash

RAW="Brown.goldtags.train"
STRIPPED=${RAW}.stripped

SCRIPT_DIR="../../scripts"

STRIP_ROOT=${SCRIPT_DIR}/strip_root.py
STRIP_FUNCTIONAL=${SCRIPT_DIR}/strip_functional.py
ENSURE_TOP=${SCRIPT_DIR}/ensure_top.py

python $STRIP_ROOT --symbol TOP < $RAW | python $STRIP_FUNCTIONAL | python $ENSURE_TOP > $STRIPPED
