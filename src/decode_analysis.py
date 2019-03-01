
# coding: utf-8

import load_corpora
from evaluate import evalb_from_files
from copy import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas
import trees
from span_length_breakdown import get_span_counts
import os.path

def label_scatter(df, x_label='word_vocab', y_label='fscore', ax=None, color='b', **kwargs):
    if ax is None:
        fig, ax = plt.subplots(figsize=(16,9))
    df.plot.scatter(x_label, y_label, ax=ax, c=color, **kwargs)
    for k, v in df.reset_index().iterrows():
        ax.annotate(v['corpus_name'], (v[x_label], v[y_label]))
    return ax

def plot(grouped_decodes, x_label='word_vocab', y_label='fscore', parser_type_pred=lambda p: p == 'inorder', best_fit=False, corpora_filter=None):
    grouped_decodes = grouped_decodes[~grouped_decodes[y_label].isnull()]
    if corpora_filter is not None:
        grouped_decodes = grouped_decodes[grouped_decodes.index.get_level_values('corpus_name').isin(corpora_filter)]
    colors = ['r', 'g', 'b', 'y']
    ix = 0
    ax = None
    has_corpora = None
    for key, group in grouped_decodes.groupby(['lex_rep', 'parser']):
        color = colors[min(ix, len(colors) - 1)]
        if not parser_type_pred(key[1]):
            continue
        if has_corpora is None:
            has_corpora = set(group.index.get_level_values('corpus_name'))
        else:
            has_corpora = has_corpora & set(group.index.get_level_values('corpus_name'))
            
    group_sizes = []
    for key, group in grouped_decodes.groupby(['lex_rep', 'parser']):
        if not parser_type_pred(key[1]):
            continue
        group = group[group.index.get_level_values('corpus_name').isin(has_corpora)]
        color = colors[min(ix, len(colors) - 1)]
        group_sizes.append(len(group))
        ax = label_scatter(group, x_label=x_label, y_label=y_label, color=color, ax=ax, label=' '.join(key))
        x = group[x_label]
        y = group[y_label]
        if best_fit:
            coeff = np.polyfit(x, y, 1)
            print("{} best fit: {}".format(key, coeff))
            ax.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color=color)
        ix += 1
    if group_sizes:
        assert all(x == group_sizes[0] for x in group_sizes[1:])
    print("group sizes: {}".format(group_sizes))


def get_predicted_file(corpus_name, model_name):
    return '../decodes/{}-{}_pred-tag-replaced.test.txt'.format(corpus_name, model_name)


def get_decode_stats(models, corpora_names=load_corpora.CORPORA_FILES.keys(), include_length_analysis=False):
    decode_stats = []
    for corpus_name in corpora_names:
        gold_file = load_corpora.CORPORA_FILES[corpus_name]
        if include_length_analysis:
            gold_trees = trees.load_trees(gold_file)
        for model in models:
            print()
            print("{}: {}".format(corpus_name, model['name']))
            data = copy(model)
            normed_corpus_name = load_corpora.DECODE_NAME_NORM[corpus_name]
            pred_file = get_predicted_file(normed_corpus_name, model['name'])
            if not os.path.exists(pred_file):
                print("decode file {} does not exist".format(pred_file))
                continue
            if include_length_analysis:
                pred_trees = trees.load_trees(pred_file)

            fscore, invalid_counts, read_and_valid = evalb_from_files(
                pred_file, gold_file
            )
            data['recall'] = fscore.recall
            data['precision'] = fscore.precision
            data['fscore'] = fscore.fscore
            data['complete_match'] = fscore.complete_match
            data['tagging_accuracy'] = fscore.tagging_accuracy
            data['error_count'] = invalid_counts.error_sentence_count
            data['skip_count'] = invalid_counts.skip_sentence_count
            
            data['corpus_name'] = corpus_name
            data['gold_file'] = gold_file
            data['pred_file'] = pred_file

            if include_length_analysis:
                data['span_counts'] = get_span_counts(gold_trees, pred_trees)

            decode_stats.append(data)
    return decode_stats


# shift_reduce_models = []
# for system in TRANSITION_SYSTEMS:
#     for lex_rep in LEX_REPS:
#         for seed in range(1, SEEDS+1):
#             model_name = "{}-{}-seed={}-beam={}".format(system, lex_rep, seed, BEAM_SIZE)
#             d = {
#                 'name': model_name,
#                 'parser': system,
#                 'seed': seed,
#                 'beam_size': BEAM_SIZE,
#                 'lex_rep': lex_rep,
#             }
#             shift_reduce_models.append(d)


# chart_models = []
# for system in ['chart']:
#     for seed in range(1, 2):
#         model_name = "{}-seed={}".format(system, seed)
#         d = {
#             'name': model_name,
#             'parser': system,
#             'seed': seed,
#             'lex_rep': 'bert',
#         }
#         chart_models.append(d)

# charniak_decode_stats = [
#     {
#         'fscore': fscore,
#         'corpus_name': corpus,
#         'parser': 'charniak',
#         'seed': 1,
#         'lex_rep': 'words'
#     }
#     for (corpus, fscore) in [
#         # Table 5 of http://www.aclweb.org/anthology/D12-1096
#         ('wsj_test', 92.07),
#         ('brown_cf', 85.91),
#         ('brown_cg', 84.56),
#         ('brown_ck', 84.09),
#         ('brown_cl', 83.95),
#         ('brown_cm', 84.65),
#         ('brown_cn', 85.20),
#         ('brown_cp', 84.09),
#         ('brown_cr', 83.60),
#         ('ewt_weblog_dev', 84.15),
#         ('ewt_weblog_email', 81.18),
#     ]
# ]


# sancl_best_decode_stats = [
#     {
#         'fscore': fscore,
#         'corpus_name': corpus,
#         'parser': 'sancl_best',
#         'seed': 1,
#         'lex_rep': 'words',
#     }
#     for (corpus, fscore) in [
#         ('ewt_answers_test', 82.19),
#         ('ewt_newsgroup_test', 84.33),
#         ('ewt_reviews_test', 84.03),
#         ('wsj_test', 90.53),
#     ]
# ]


# sancl_berkeley_decode_stats = [
#     {
#         'fscore': fscore,
#         'corpus_name': corpus,
#         'parser': 'berkeley',
#         'seed': 1,
#         'lex_rep': 'words',
#     }
#     for (corpus, fscore) in [
#         ('ewt_answers_test', 75.92),
#         ('ewt_newsgroup_test', 78.14),
#         ('ewt_reviews_test', 77.16),
#         ('wsj_test', 88.21),
#     ]
# ]


# decodes = pandas.DataFrame(decode_stats + charniak_decode_stats + sancl_best_decode_stats + sancl_berkeley_decode_stats)


# decodes[decodes.parser=='chart']


# decodes[decodes.fscore.isnull()][['corpus_name', 'lex_rep', 'parser', 'seed']]


# from corpora_stats import histogram_intersection, counts_intersection_rescale, counts_intersection_norescale


# # In[22]:


# counts_intersection_rescale


# # In[23]:


# SANCL_CORPORA = ['ewt_answers_test', 'ewt_newsgroup_test', 'ewt_reviews_test', 'wsj_test']


# # In[24]:


# from load_corpora import CORPORA_FILES


# # In[25]:


# JONO_CORPORA = ['wsj_test'] + [corpus for corpus in CORPORA_FILES if corpus.startswith("brown")]


# # In[26]:


# # TODO: merge to corpora_stats
# CORPUS_STAT_COLS = ['word_vocab', 'productions', 'multi_word_productions', 'multi_word_span_labels', 'length_hist_intersection']


# # In[27]:


# EVALB_COLS = ['fscore', 'complete_match', 'tagging_accuracy', 'skip_count']


# # In[28]:


# RESCALE = False


# # In[29]:


# counts_intersection_norescale['word_vocab'].corr(counts_intersection_norescale['productions'], method='spearman')


# # In[30]:


# counts_intersection_norescale['word_vocab'].corr(counts_intersection_norescale['multi_word_productions'], method='spearman')


# # In[31]:


# counts_intersection_norescale['word_vocab'].corr(counts_intersection_norescale['multi_word_span_labels'], method='spearman')


# # In[32]:


# counts_intersection_norescale['word_vocab'].corr(counts_intersection_norescale['length_hist_intersection'], method='spearman')


# # In[125]:


# decodes_merged = decodes.merge(counts_intersection_rescale if RESCALE else counts_intersection_norescale , left_on='corpus_name', right_on='name')


# # In[126]:


# grouped_decodes = decodes_merged.groupby(['corpus_name', 'lex_rep', 'parser'])[EVALB_COLS + CORPUS_STAT_COLS].mean()


# # In[127]:


# grouped_decodes[-grouped_decodes['fscore'].isnull()]


# # In[128]:


# import matplotlib.pyplot as plt


# # In[129]:


# # In[132]:


# grouped_decodes.columns


# # In[133]:


# from IPython.display import set_matplotlib_formats


# # In[134]:


# set_matplotlib_formats('png', 'pdf')


# # In[135]:


# plot(grouped_decodes, best_fit=True, parser_type_pred=lambda p: p == 'inorder')


# # In[136]:


# plot(grouped_decodes, best_fit=True, parser_type_pred=lambda p: p == 'inorder' or p == 'sancl_best')


# # In[137]:


# plot(grouped_decodes, best_fit=True, parser_type_pred=lambda p: p == 'inorder' or p == 'berkeley')


# # In[138]:


# plot(grouped_decodes, best_fit=True, parser_type_pred=lambda p: p == 'inorder' or p == 'charniak')


# # In[143]:


# plot(grouped_decodes[grouped_decodes.index.get_level_values('lex_rep') == 'bert'], best_fit=True, parser_type_pred=lambda p: p == 'inorder' or p == 'chart' or p == 'topdown')


# # In[113]:


# plot(grouped_decodes[grouped_decodes.index.get_level_values('lex_rep').isin(['pos', 'bert'])], y_label='complete_match', best_fit=True, parser_type_pred=lambda p: p == 'inorder' or p == 'topdown')


# # In[115]:


# plot(grouped_decodes, y_label='fscore', best_fit=True, parser_type_pred=lambda p: p == 'topdown')


# # In[116]:


# CORPUS_STAT_COLS


# # In[118]:


# plot(grouped_decodes.dropna(), x_label='length_hist_intersection', best_fit=True, parser_type='inorder')


# # In[119]:


# plot(grouped_decodes.dropna(), x_label='productions', best_fit=True, parser_type='inorder')


# # In[124]:


# plot(grouped_decodes[~grouped_decodes.index.get_level_values('corpus_name').str.startswith("genia_")].dropna(), x_label='word_vocab', y_label='complete_match', best_fit=True, parser_type='inorder')


# # In[125]:


# plot(grouped_decodes.dropna(), x_label='word_vocab', y_label='complete_match', best_fit=True, parser_type='inorder')

