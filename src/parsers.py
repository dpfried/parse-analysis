import os.path

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


ALL_MODELS = CHART_MODELS + SHIFT_REDUCE_MODELS

def get_predicted_file(corpus_name, model_name, decodes_root='../decodes/'):
    return os.path.join(decodes_root, '{}-{}_pred-tag-replaced.test.txt'.format(corpus_name, model_name))
