from collections import Counter, namedtuple
import functools

import numpy as np

import trees
import load_corpora

SpanCounts = namedtuple("SpanCounts", ["lengths", "match_counts", "gold_counts", "pred_counts"])

SpanF1s = namedtuple("SpanF1s", ["lengths", "f1s", "recalls", "precisions"])

SpanCumulativeF1s = namedtuple("SpanF1s", ["lengths", "f1s", "match_counts", "recalls", "gold_counts", "precisions", "pred_counts"])

# %%

# Based on COLLINS_ch.prm
DELETE_LABELS = set(".,:") | set(["``", "''", "PU"])

PRT_TO_ADVP = True

def convert_label(label):
    if PRT_TO_ADVP and label == 'PRT':
        return 'ADVP'
    else:
        return label


def all_spans(tree, delete_labels=(), del_word_mask=None, add_multiplicities=True):
    if isinstance(tree, (trees.InternalTreebankNode, trees.LeafTreebankNode)):
        return all_spans(tree.convert(), delete_labels, del_word_mask, add_multiplicities=add_multiplicities)
    elif isinstance(tree, trees.LeafParseNode):
        return []
    else:
        label = tuple([convert_label(l) for l in tree.label if l != 'TOP'])
        if label and del_word_mask is None:
            res = [(tree.left, tree.right, sublabel)
                   for sublabel in label
                   if sublabel not in delete_labels]
        elif label:
            left, right = tree.left, tree.right
            while left < len(del_word_mask) and del_word_mask[left]:
                left += 1
            while right > 0 and del_word_mask[right - 1]:
                right -= 1
            res = []
            if left < right:
                for sublabel in set(label) if add_multiplicities else label:
                    if sublabel in delete_labels:
                        continue
                    if add_multiplicities:
                        for multiplicity in range(label.count(sublabel)):
                            if multiplicity == 0:
                                res.append((left, right, sublabel))
                            else:
                                res.append((left, right, sublabel + "[{}]".format(multiplicity)))
                    else:
                        res.append((left, right, sublabel))
        else:
            res = []

        for child in tree.children:
            res += all_spans(child, delete_labels, del_word_mask, add_multiplicities=add_multiplicities)

        return res

# %%

def count_matched_spans(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
    matched_by_len = Counter()
    unmatched_by_len = Counter()

    for gold_tree, pred_tree in zip(gold_trees, pred_trees):
        if delete_labels:
            del_word_mask = [(leaf.tag in delete_labels) for leaf in list(gold_tree.leaves())]
        else:
            del_word_mask = None
        gold_spans = all_spans(gold_tree, delete_labels, del_word_mask, add_multiplicities=True)
        pred_spans = all_spans(pred_tree, delete_labels, del_word_mask, add_multiplicities=True)

        matched_spans = [span for span in gold_spans if span in pred_spans]
        unmatched_spans = [span for span in gold_spans if span not in pred_spans]

        for left, right, _ in matched_spans:
            matched_by_len[right - left] += 1

        for left, right, _ in unmatched_spans:
            unmatched_by_len[right - left] += 1

    return matched_by_len, unmatched_by_len

def count_matched_spans_gold_and_pred(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
    matched_by_len = Counter()
    pred_by_len = Counter()
    gold_by_len = Counter()

    for i, (gold_tree, pred_tree) in enumerate(zip(gold_trees, pred_trees)):
        try:
            if delete_labels:
                del_word_mask = [(leaf.tag in delete_labels) for leaf in list(gold_tree.leaves())]
            else:
                del_word_mask = None
            gold_spans = Counter(all_spans(gold_tree, delete_labels, del_word_mask, add_multiplicities=False))
            pred_spans = Counter(all_spans(pred_tree, delete_labels, del_word_mask, add_multiplicities=False))

            for gs, gold_count in gold_spans.items():
                left, right, _ = gs
                gold_by_len[right - left] += gold_count
                if gs in pred_spans:
                    matched_by_len[right - left] += min(gold_count, pred_spans[gs])

            for ps, pred_count in pred_spans.items():
                left, right, _ = ps
                pred_by_len[right - left] += pred_count
        except Exception as e:
            print("span count exception for tree index {}".format(i))
            print(e)

    return matched_by_len, gold_by_len, pred_by_len


# %%

def get_span_accuracies(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
    matched_by_len, unmatched_by_len = count_matched_spans(gold_trees, pred_trees, delete_labels)

    xs = []
    ys = []
    for x in range(1, 200):
        try:
            y = matched_by_len[x] / (matched_by_len[x] + unmatched_by_len[x])
        except ZeroDivisionError:
            continue
        xs.append(x)
        ys.append(y)

    return xs, ys


# %%

def get_span_accuracies_gte(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
    matched_by_len, unmatched_by_len = count_matched_spans(gold_trees, pred_trees, delete_labels)

    xs = []
    ys_numer = []
    ys_denom = []
    for x in range(1, 200):
        y_numer = matched_by_len[x]
        y_denom = matched_by_len[x] + unmatched_by_len[x]
        if y_denom > 0:
            xs.append(x)
            ys_numer.append(y_numer)
            ys_denom.append(y_denom)
        else:
            continue

    ys_numer = np.cumsum(ys_numer[::-1])[::-1]
    ys_denom = np.cumsum(ys_denom[::-1])[::-1]
    ys = np.array(ys_numer) / np.array(ys_denom)

    return xs, ys


def get_span_counts(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
    matched_by_len, gold_by_len, pred_by_len = count_matched_spans_gold_and_pred(
        gold_trees, pred_trees, delete_labels=delete_labels
    )

    xs = []
    match_counts = []
    gold_counts = []
    pred_counts = []

    for x in range(1, max(max(gold_by_len.values()), max(pred_by_len.values())) + 1):
        gold = gold_by_len[x]
        pred = pred_by_len[x]
        matched = matched_by_len[x]
        if gold == 0 or pred == 0:
            assert matched == 0
        if gold > 0 or pred > 0:
            xs.append(x)
            match_counts.append(matched)
            gold_counts.append(gold)
            pred_counts.append(pred)
        else:
            continue

    return SpanCounts(
        lengths=np.array(xs),
        match_counts=np.array(match_counts),
        gold_counts=np.array(gold_counts),
        pred_counts=np.array(pred_counts)
    )


def get_span_f1s_from_counts(span_counts):
    rs = span_counts.match_counts / span_counts.gold_counts
    ps = span_counts.match_counts / span_counts.pred_counts
    fs = (2 * rs * ps) / (rs + ps)
    return SpanF1s(lengths=span_counts.lengths, f1s=fs, recalls=rs, precisions=ps)

def get_span_f1s_gte_from_counts(span_counts):
    match_cum = np.cumsum(span_counts.match_counts[::-1])[::-1]
    gold_cum = np.cumsum(span_counts.gold_counts[::-1])[::-1]
    pred_cum = np.cumsum(span_counts.pred_counts[::-1])[::-1]

    rs = match_cum / gold_cum
    ps = match_cum / pred_cum
    fs = (2 * rs * ps) / (ps + rs)

    return SpanCumulativeF1s(
        lengths=span_counts.lengths,
        f1s=fs, match_counts=match_cum,
        recalls=rs, gold_counts=gold_cum,
        precisions=ps, pred_counts=pred_cum
    )

def get_span_f1s(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
    return get_span_f1s_from_counts(*get_span_counts(gold_trees, pred_trees, delete_labels=delete_labels))

def get_span_f1s_gte(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
     return get_span_f1s_gte_from_counts(*get_span_counts(gold_trees, pred_trees, delete_labels=delete_labels))

# %%

def main():
    gold_trees = trees.load_trees(load_corpora.CORPORA_FILES['brown_train'])
    pred_trees = gold_trees # To demo the API

    pred_xy = get_span_accuracies(gold_trees, pred_trees)
    pred_xy_gte = get_span_accuracies_gte(gold_trees, pred_trees)

    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot(*pred_xy, label='perfect')
    plt.legend()

    plt.figure()
    plt.plot(*pred_xy_gte, label='perfect')
    plt.legend()

if __name__ == '__main__':
    main()
