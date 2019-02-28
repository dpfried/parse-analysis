from collections import Counter
import functools

import numpy as np

import trees
import load_corpora

# %%

# Based on COLLINS_ch.prm
DELETE_LABELS = set(".,:") | set(["``", "''", "PU"])

def all_spans(tree, delete_labels=(), del_word_mask=None):
    if isinstance(tree, (trees.InternalTreebankNode, trees.LeafTreebankNode)):
        return all_spans(tree.convert(), delete_labels, del_word_mask)
    elif isinstance(tree, trees.LeafParseNode):
        return []
    else:
        label = tuple([l for l in tree.label if l != 'TOP'])
        if label and del_word_mask is None:
            res = [(tree.left, tree.right, label)]
        elif label:
            left, right = tree.left, tree.right
            while left < len(del_word_mask) and del_word_mask[left]:
                left += 1
            while right > 0 and del_word_mask[right - 1]:
                right -= 1
            res = []
            if left < right:
                for sublabel in set(label):
                    if sublabel in delete_labels:
                        continue
                    for multiplicity in range(label.count(sublabel)):
                        if multiplicity == 0:
                            res.append((left, right, sublabel))
                        else:
                            res.append((left, right, sublabel + "[{}]".format(multiplicity)))
        else:
            res = []

        for child in tree.children:
            res += all_spans(child, delete_labels, del_word_mask)

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
        gold_spans = all_spans(gold_tree, delete_labels, del_word_mask)
        pred_spans = all_spans(pred_tree, delete_labels, del_word_mask)

        matched_spans = [span for span in gold_spans if span in pred_spans]
        unmatched_spans = [span for span in gold_spans if span not in pred_spans]

        for left, right, _ in matched_spans:
            matched_by_len[right - left] += 1

        for left, right, _ in unmatched_spans:
            unmatched_by_len[right - left] += 1

    return matched_by_len, unmatched_by_len

# %%

def get_span_accuracies(gold_trees, pred_trees, delete_labels=DELETE_LABELS):
    matched_by_len, unmatched_by_len = count_matched_spans(gold_trees, pred_trees, delete_labels)

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
