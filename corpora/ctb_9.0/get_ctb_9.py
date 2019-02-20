# coding: utf-8

import nltk
from nltk.corpus import BracketParseCorpusReader, LazyCorpusLoader
import sys
import itertools
sys.path.append("../ctb_5.1/")
import process_ctb

corpus_root = "/home/dfried/data/ctb_9.0/data/"
nltk_out_root = "/home/dfried/nltk_data/corpora/ctb_9.0/"

process_ctb.convert(corpus_root, nltk_out_root, encoding='utf-8', filter_fn=lambda _: True)

ctb_9 = LazyCorpusLoader("ctb_9.0", BracketParseCorpusReader, r'chtb_.*', tagset='unknown')

# 541-554 are not mentioned in the CTB 9.0 readme, but are present
training = [(1, 270), (440, 454), (500, 540), (541, 554), (590, 596), (600, 885), (900, 931), (1001, 1151)]
development = [(301, 325)]
test = [(271, 300)] 

other_splits = {
    'newswire': [(4000, 4050)],
    'broadcast_news': [(2000, 3145), (4051, 4111)],
    'broadcast_conversations': [(4112, 4197)],
    'weblogs': [(4198, 4411)],
    'discussion_forums': [(5000, 5558)],
    'chat_messages': [(6000, 6700)],
    'conversational_speech': [(7000, 7017)]
}

def files_from_boundaries(boundaries_list):
    l = []
    for boundaries in boundaries_list:
        l += list(range(boundaries[0], boundaries[1] + 1))
    return l

# make sure there's no overlap
for bound_l_1, bound_l_2 in itertools.combinations([training, development, test] + list(other_splits.values()), 2):
    files_1 = files_from_boundaries(bound_l_1)
    files_2 = files_from_boundaries(bound_l_2)
    assert not (set(files_1) & set(files_2))

process_ctb.combine_fids(ctb_9, nltk_out_root, files_from_boundaries(training), 'train.gold.original', suffix_glob='*', pad_hundreds=True)
process_ctb.combine_fids(ctb_9, nltk_out_root, files_from_boundaries(development), 'dev.gold.original', suffix_glob='*', pad_hundreds=True)
process_ctb.combine_fids(ctb_9, nltk_out_root, files_from_boundaries(test), 'test.gold.original', suffix_glob='*', pad_hundreds=True)
for split, boundaries in other_splits.items():
    process_ctb.combine_fids(ctb_9, nltk_out_root, files_from_boundaries(boundaries), '{}.gold.original'.format(split), suffix_glob='*', pad_hundreds=True)
