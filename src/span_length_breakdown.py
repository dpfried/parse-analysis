from collections import Counter
import functools

import numpy as np

import trees
import load_corpora

# %%

def all_spans(tree):
    if isinstance(tree, (trees.InternalTreebankNode, trees.LeafTreebankNode)):
        return all_spans(tree.convert())
    elif isinstance(tree, trees.LeafParseNode):
        return []
    else:
        label = tuple([l for l in tree.label if l != 'TOP'])
        if label:
            res = [(tree.left, tree.right, label)]
        else:
            res = []
        for child in tree.children:
            res += all_spans(child)
        return res

# %%

def count_matched_spans(gold_trees, pred_trees):
    matched_by_len = Counter()
    unmatched_by_len = Counter()

    for gold_tree, pred_tree in zip(gold_trees, pred_trees):
        gold_spans = all_spans(gold_tree)
        pred_spans = all_spans(pred_tree)

        matched_spans = [span for span in gold_spans if span in pred_spans]
        unmatched_spans = [span for span in gold_spans if span not in pred_spans]

        for left, right, _ in matched_spans:
            matched_by_len[right - left] += 1

        for left, right, _ in unmatched_spans:
            unmatched_by_len[right - left] += 1

    return matched_by_len, unmatched_by_len

# %%

def get_span_accuracies(gold_trees, pred_trees):
    matched_by_len, unmatched_by_len = count_matched_spans(gold_trees, pred_trees)

    xs = []
    ys = []
    for x in range(1, 200):
        try:
            y = matched_by_len[x] / (matched_by_len[x] + unmatched_by_len[x])
        except ZeroDivisionError:
            break
        xs.append(x)
        ys.append(y)

    return xs, ys

# %%

def get_span_accuracies_gte(gold_trees, pred_trees):
    matched_by_len, unmatched_by_len = count_matched_spans(gold_trees, pred_trees)

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
            break

    ys_numer = np.cumsum(ys_numer[::-1])[::-1]
    ys_denom = np.cumsum(ys_denom[::-1])[::-1]
    ys = np.array(ys_numer) / np.array(ys_denom)

    return xs, ys

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
