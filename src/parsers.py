import os.path

def get_predicted_file(corpus_name, model_name, decodes_root='../decodes/'):
    return os.path.join(decodes_root, '{}-{}_pred-tag-replaced.test.txt'.format(corpus_name, model_name))

LEX_REPS = ["bert", "pos", "emb-pos"]

TRANSITION_SYSTEMS = ["inorder", "topdown"]

BEAM_SIZE = 10

SHIFT_REDUCE_SEEDS = [1,2,3,4,5]

SHIFT_REDUCE_MODELS = []
for system in TRANSITION_SYSTEMS:
    for lex_rep in LEX_REPS:
        for seed in SHIFT_REDUCE_SEEDS:
            model_name = "{}-{}-seed={}-beam={}".format(system, lex_rep, seed, BEAM_SIZE)
            d = {
                'name': model_name,
                'parser': system,
                'seed': seed,
                'beam_size': BEAM_SIZE,
                'lex_rep': lex_rep,
            }
            SHIFT_REDUCE_MODELS.append(d)

CHART_MODELS = []

CHART_SEEDS = [1,2,3,4,5]
for system in ['chart', 'chartlstm']:
    for seed in CHART_SEEDS:
        model_name = "{}-seed={}".format(system, seed)
        d = {
            'name': model_name,
            'parser': system,
            'seed': seed,
            'lex_rep': 'bert' if system == 'chart' else 'lstm',
        }
        CHART_MODELS.append(d)


CHARNIAK_MODELS = []
CHARNIAK_CONDITIONS = ["WSJ-PTB3", "WSJ-PTB3-no-rerank",
                       #"WSJ+Gigaword",
                       "WSJ+Gigaword-v2",
                       #"SANCL2012-Uniform", "GENIA+PubMed"
                       ]
for condition in CHARNIAK_CONDITIONS:
    model_name = "charniak-{}".format(condition)
    d = {
        'name': model_name,
        'parser': model_name,
        'seed': 1,
        'lex_rep': 'words',
    }
    CHARNIAK_MODELS.append(d)


ZPAR_MODELS = [
    {
        'name': 'zpar',
        'parser': 'zpar',
        'seed': 1,
        'lex_rep': 'words'
    }
]

ENGLISH_MODELS = SHIFT_REDUCE_MODELS + CHART_MODELS + CHARNIAK_MODELS
CHINESE_MODELS = SHIFT_REDUCE_MODELS + [model for model in CHART_MODELS if model['parser'] != 'chartlstm'] + ZPAR_MODELS

CHARNIAK_REPORTED = [
    {
        'fscore': fscore,
        'corpus_name': corpus,
        'parser': 'charniak-rep',
        'seed': 1,
        'lex_rep': 'words'
    }
    for (corpus, fscore) in [
        # Table 5 of http://www.aclweb.org/anthology/D12-1096
        ('wsj_test', 92.07),
        ('brown_cf', 85.91),
        ('brown_cg', 84.56),
        ('brown_ck', 84.09),
        ('brown_cl', 83.95),
        ('brown_cm', 84.65),
        ('brown_cn', 85.20),
        ('brown_cp', 84.09),
        ('brown_cr', 83.60),
        ('ewt_weblog_dev', 84.15),
        ('ewt_weblog_email', 81.18),
    ]
]

SANCL_BEST_DECODE_STATS = [
    # https://sites.google.com/site/sancl2012/home/shared-task/results
    {
        'fscore': fscore,
        'corpus_name': corpus,
        'parser': 'sancl-rep',
        'seed': 1,
        'lex_rep': 'words',
    }
    for (corpus, fscore) in [
        ('ewt_answers_test', 82.19),
        ('ewt_newsgroup_test', 84.33),
        ('ewt_reviews_test', 84.03),
        ('wsj_test', 90.53),
    ]
]

SANCL_BERKELEY_DECODE_STATS = [
    # https://sites.google.com/site/sancl2012/home/shared-task/results
    {
        'fscore': fscore,
        'corpus_name': corpus,
        'parser': 'berkeley-rep',
        'seed': 1,
        'lex_rep': 'words',
    }
    for (corpus, fscore) in [
        ('ewt_answers_test', 75.92),
        ('ewt_newsgroup_test', 78.14),
        ('ewt_reviews_test', 77.16),
        ('wsj_test', 88.21),
    ]
]


ALL_MODELS = CHART_MODELS + SHIFT_REDUCE_MODELS + CHARNIAK_MODELS + \
             CHARNIAK_REPORTED + SANCL_BEST_DECODE_STATS + SANCL_BERKELEY_DECODE_STATS
