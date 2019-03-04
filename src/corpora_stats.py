from collections import Counter
import functools

import evaluate
import trees
import load_corpora

import pandas

# %%

CORPORA = load_corpora.get_corpora()
CORPORA_DESCRIPTIONS = load_corpora.get_corpora_descriptions()

# %%

def histogram_intersection(counter_a, counter_b):
    total_a = float(sum(counter_a.values()))
    total_b = float(sum(counter_b.values()))

    res = 0.
    for k in counter_a.keys() & counter_b.keys():
        res += min(counter_a[k] / total_a, counter_b[k] / total_b)
    return res

# %%

@functools.lru_cache()
def length_rescaling_fators(src_treebank, tgt_treebank):
    lengths_src = Counter()
    for tree in src_treebank:
        lengths_src[len(list(tree.leaves()))] += 1
    lengths_tgt = Counter()
    for tree in tgt_treebank:
        lengths_tgt[len(list(tree.leaves()))] += 1

    total_src = float(sum(lengths_src.values()))
    total_tgt = float(sum(lengths_tgt.values()))

    importance_by_length = {}
    for length in lengths_tgt:
        if length not in lengths_src:
            importance_by_length[length] = 0
            continue

        importance_by_length[length] =  (lengths_src[length] / total_src) / (lengths_tgt[length] / total_tgt)

    importance_by_tree = {}
    for tree in tgt_treebank:
        importance_by_tree[tree] = importance_by_length[len(list(tree.leaves()))]

    return importance_by_tree

# %%

class CorporaCounts(object):
    def __init__(self, corpora, length_rescale_for=None):
        self.corpora = corpora
        self.length_rescale = length_rescale_for is not None
        self.length_rescale_for = length_rescale_for

    @property
    @functools.lru_cache()
    def vocabs(self):
        res = {}
        for name, treebank in self.corpora.items():
            if self.length_rescale:
                weights = length_rescaling_fators(self.length_rescale_for, treebank)
            counter = Counter()
            for tree in treebank:
                for leaf in tree.leaves():
                    counter[leaf.word] += weights[tree] if self.length_rescale else 1
            res[name] = counter
        return res

    @property
    @functools.lru_cache()
    def lengths(self):
        res = {}
        for name, treebank in self.corpora.items():
            if self.length_rescale:
                weights = length_rescaling_fators(self.length_rescale_for, treebank)
            counter = Counter()
            for tree in treebank:
                counter[len(list(tree.leaves()))] += weights[tree] if self.length_rescale else 1
            res[name] = counter
        return res

    @property
    @functools.lru_cache()
    def _structural_counters(self):
        #TODO update this for CTB
        PUNCT = set(".,:#$") | set(["-LRB-", "-RRB-", "-LCB-", "-RCB-", "-LSB-", "-RSB-", "``", "''"])

        def accumulate(tree, weight, counters, index=0):
            c, multiword_c, label_c = counters
            if isinstance(tree, trees.LeafTreebankNode):
                return index + 1

            index_right = index
            children = []
            for child in tree.children:
                index_right = accumulate(child, weight, counters, index=index_right)
                if not (isinstance(child, trees.LeafTreebankNode) and child.tag in PUNCT):
                    children.append(child)

            production = (
                tree.label.split('-')[0],
                tuple([getattr(child, 'label', 'WORD').split('-')[0] for child in children]))
            c[production] += weight

            if index_right - index > 1:
                multiword_c[production] += weight
                label_c[production[0]] += weight

            return index_right

        multiword_label_counters = {}
        production_counters = {}
        multiword_production_counters = {}
        for name, treebank in self.corpora.items():
            if self.length_rescale:
                weights = length_rescaling_fators(self.length_rescale_for, treebank)

            c = Counter()
            multiword_c = Counter()
            label_c = Counter()
            counters = (c, multiword_c, label_c)

            for tree in treebank:
                weight = weights[tree] if self.length_rescale else 1
                accumulate(tree, weight, counters)

            production_counters[name] = c
            multiword_production_counters[name] = multiword_c
            multiword_label_counters[name] = label_c

        return multiword_label_counters, production_counters, multiword_production_counters

    @property
    def multiword_labels(self):
        return self._structural_counters[0]

    @property
    def productions(self):
        return self._structural_counters[1]

    @property
    def multiword_productions(self):
        return self._structural_counters[2]

def generate_counts_intersection_frames():
    counts_norescale = CorporaCounts(CORPORA)
    counts_rescale = CorporaCounts(CORPORA, length_rescale_for=CORPORA['wsj_train'])

    counts_intersection_frames = {}
    for (counts, count_name) in [(counts_norescale, "norescale"), (counts_rescale, "rescale")]:
        for (lang_corpora, lang_name, reference_corpus) in [
            (load_corpora.ENGLISH_CORPORA_NAMES, "english", "wsj_train"),
            (load_corpora.CHINESE_CORPORA_NAMES, "chinese", "ctb_5.1_train")
        ]:
            by_corpus = {}
            for k in lang_corpora:
                by_corpus[k] = {'name': k}

            if counts == counts_norescale:
                print('{} [no rescale]'.format(lang_name))
            else:
                print('{} [rescaled to match training length distribution]'.format(lang_name))

            print('# Word vocabularies')
            for k in lang_corpora:
                val = histogram_intersection(counts.vocabs[reference_corpus], counts.vocabs[k])
                by_corpus[k]['word_vocab'] = val
                print(f'{CORPORA_DESCRIPTIONS[k]: <20} {val:.2f}')

            print()
            print()
            print('# Productions')
            for k in lang_corpora:
                val = histogram_intersection(counts.productions[reference_corpus], counts.productions[k])
                by_corpus[k]['productions'] = val
                print(f'{CORPORA_DESCRIPTIONS[k]: <20} {val:.2f}')

            print()
            print()
            print('# Multi-word productions')
            for k in lang_corpora:
                val = histogram_intersection(counts.multiword_productions[reference_corpus], counts.multiword_productions[k])
                by_corpus[k]['multi_word_productions'] = val
                print(f'{CORPORA_DESCRIPTIONS[k]: <20} {val:.2f}')

            print()
            print()
            print('# Multi-word span labels')
            for k in lang_corpora:
                val = histogram_intersection(counts.multiword_labels[reference_corpus], counts.multiword_labels[k])
                by_corpus[k]['multi_word_span_labels'] = val
                print(f'{CORPORA_DESCRIPTIONS[k]: <20} {val:.2f}')

            print()
            print()
            print('# Average length')
            for k in lang_corpora:
                val = sum([kk * vv for kk, vv in counts.lengths[k].items()]) / sum(counts.lengths[k].values())
                by_corpus[k]['length'] = val
                print(f'{CORPORA_DESCRIPTIONS[k]: <20} {val:.2f}')

            print()
            print()
            print('# Length histogram intersection')
            for k in lang_corpora:
                val = histogram_intersection(counts.lengths[reference_corpus], counts.lengths[k])
                by_corpus[k]['length_hist_intersection'] = val
                print(f'{CORPORA_DESCRIPTIONS[k]: <20} {val:.2f}')

            print()
            print()

            counts_intersection_frames[(lang_name, count_name)] = pandas.DataFrame(by_corpus.values())
    return counts_intersection_frames

# %%
import pickle
try:
    with open('count_intersection_frames.pkl', 'rb') as f:
        counts_intersection_frames = pickle.load(f)
except:
    counts_intersection_frames = generate_counts_intersection_frames()
    with open('count_intersection_frames.pkl', 'wb') as f:
        pickle.dump(counts_intersection_frames, f)
