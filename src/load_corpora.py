import os
import trees

BASE_PATH = os.path.join(os.path.dirname(__file__), '../corpora/')

CORPORA_FILES = {
    # 'brown': 'brown/all.stripped',
    'brown_cf': 'brown/cf.gold.stripped',
    'brown_cg': 'brown/cg.gold.stripped',
    'brown_ck': 'brown/ck.gold.stripped',
    'brown_cl': 'brown/cl.gold.stripped',
    'brown_cm': 'brown/cm.gold.stripped',
    'brown_cn': 'brown/cn.gold.stripped',
    'brown_cp': 'brown/cp.gold.stripped',
    'brown_cr': 'brown/cr.gold.stripped',
    'brown_train': 'brown/train.gold.stripped',
    # 'brown_test': 'brown/test.gold.stripped',
    # 'brown_test40': 'brown/test40.gold.stripped',
    'genia_train': 'genia/train.gold.stripped',
    'genia_dev': 'genia/dev.gold.stripped',
    # 'genia_test': 'genia/test.gold.stripped',
    # 'wsj_train': 'wsj_ch/train.stripped',
    # 'wsj_dev': 'wsj_ch/dev.stripped',
    # 'wsj_test': 'wsj_ch/test.stripped',
    'wsj_train': 'wsj_pred_tags/train.gold.stripped',
    'wsj_dev': 'wsj_pred_tags/dev.gold.stripped',
    'wsj_test': 'wsj_pred_tags/test.gold.stripped',
    'ewt_answers_dev': 'ewt/answers.dev.gold.stripped',
    'ewt_answers_test': 'ewt/answers.test.gold.stripped',
    'ewt_email_dev': 'ewt/email.dev.gold.stripped',
    'ewt_email_test': 'ewt/email.test.gold.stripped',
    'ewt_newsgroup_dev': 'ewt/newsgroup.dev.gold.stripped',
    'ewt_newsgroup_test': 'ewt/newsgroup.test.gold.stripped',
    'ewt_reviews_dev': 'ewt/reviews.dev.gold.stripped',
    'ewt_reviews_test': 'ewt/reviews.test.gold.stripped',
    'ewt_weblog_dev': 'ewt/weblog.dev.gold.stripped',
    'ewt_weblog_test': 'ewt/weblog.test.gold.stripped',
}
CORPORA_FILES = {k: os.path.join(BASE_PATH, v) for k,v in CORPORA_FILES.items()}

CORPORA = None
CORPORA_DESCRIPTIONS = {
    'brown': 'Brown (all)',
    'brown_cf': 'Brown (Popular)',
    'brown_cg': 'Brown (Biographies)',
    'brown_ck': 'Brown (General)',
    'brown_cl': 'Brown (Mystery)',
    'brown_cm': 'Brown (Science)',
    'brown_cn': 'Brown (Adventure)',
    'brown_cp': 'Brown (Romance)',
    'brown_cr': 'Brown (Humor)',
    'brown_train': 'Brown (train)',
    'brown_test': 'Brown (test)',
    'brown_test40': 'Brown (test40)',
    'genia_train': 'Genia (train)',
    'genia_dev': 'Genia (dev)',
    'genia_test': 'Genia (test)',
    'wsj_train': 'WSJ (train)',
    'wsj_dev': 'WSJ (dev)',
    'wsj_test': 'WSJ (test)',
    'ewt_answers_dev': 'EWT Answers (dev)',
    'ewt_answers_test': 'EWT Answers (test)',
    'ewt_email_dev': 'EWT Email (dev)',
    'ewt_email_test': 'EWT Email (test)',
    'ewt_newsgroup_dev': 'EWT Newsgroup (dev)',
    'ewt_newsgroup_test': 'EWT Newsgroup (test)',
    'ewt_reviews_dev': 'EWT Reviews (dev)',
    'ewt_reviews_test': 'EWT Reviews (test)',
    'ewt_weblog_dev': 'EWT Weblog (dev)',
    'ewt_weblog_test': 'EWT Weblog (test)',
}

DECODE_NAME_NORM = {
}

DECODE_NAME_UNNORM = {
}

for corpus in CORPORA_FILES:
    replaced = corpus.replace("_", "-")
    if 'ewt' in replaced:
        replaced = replaced.replace("-dev", ".dev")
        replaced = replaced.replace("-test", ".test")
    if 'wsj' in replaced:
        replaced = replaced.replace("wsj", "wsj_pred_tags")
    DECODE_NAME_NORM[corpus] = replaced
    assert replaced not in DECODE_NAME_UNNORM
    DECODE_NAME_UNNORM[replaced] = corpus

def get_corpora():
    global CORPORA
    if CORPORA is None:
        res = {}
        for k, filename in CORPORA_FILES.items():
            # Represent corpora as tuples so they can be used as keys in dicts
            res[k] = tuple(trees.load_trees(filename))
        CORPORA = res
    return CORPORA

def get_corpora_descriptions():
    return CORPORA_DESCRIPTIONS
