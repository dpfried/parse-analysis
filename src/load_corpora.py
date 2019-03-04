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
    'brown_test': 'brown/test.gold.stripped',
    'brown_test40': 'brown/test40.gold.stripped',
    'brown_all': 'brown/all.gold.stripped',

    'genia_train': 'genia/train.gold.stripped',
    'genia_dev': 'genia/dev.gold.stripped',
    'genia_test': 'genia/test.gold.stripped',
    'genia_all': 'genia/all.gold.stripped',

    # 'wsj_train': 'wsj_ch/train.stripped',
    # 'wsj_dev': 'wsj_ch/dev.stripped',
    # 'wsj_test': 'wsj_ch/test.stripped',

    'wsj_train': 'wsj_pred_tags/train.gold.stripped',
    'wsj_dev': 'wsj_pred_tags/dev.gold.stripped',
    'wsj_test': 'wsj_pred_tags/test.gold.stripped',

    'wsj_test_dis': 'wsj_pred_tags_winnow/dis.gold.stripped',
    'wsj_test_sim': 'wsj_pred_tags_winnow/sim.gold.stripped',
    'wsj_test_v0g0': 'wsj_pred_tags_winnow/v0g0.gold.stripped',
    'wsj_test_v0g1': 'wsj_pred_tags_winnow/v0g1.gold.stripped',
    'wsj_test_v1g0': 'wsj_pred_tags_winnow/v1g0.gold.stripped',
    'wsj_test_v1g1': 'wsj_pred_tags_winnow/v1g1.gold.stripped',
    'wsj_test_mwp_dis': 'wsj_pred_tags_winnow/mwp_dis.gold.stripped',
    'wsj_test_mwp_sim': 'wsj_pred_tags_winnow/mwp_sim.gold.stripped',
    'wsj_test_vocab_dis': 'wsj_pred_tags_winnow/vocab_dis.gold.stripped',
    'wsj_test_vocab_sim': 'wsj_pred_tags_winnow/vocab_sim.gold.stripped',

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
    'ewt_all': 'ewt/all.gold.stripped',

    "ctb_9.0_broadcast_conversations": "ctb_9.0/broadcast_conversations.gold.stripped",
    "ctb_9.0_broadcast_news": "ctb_9.0/broadcast_news.gold.stripped",
    "ctb_9.0_chat_messages": "ctb_9.0/chat_messages.gold.stripped",
    "ctb_9.0_conversational_speech": "ctb_9.0/conversational_speech.gold.stripped",
    "ctb_9.0_discussion_forums": "ctb_9.0/discussion_forums.gold.stripped",
    "ctb_9.0_newswire": "ctb_9.0/newswire.gold.stripped",
    "ctb_9.0_weblogs": "ctb_9.0/weblogs.gold.stripped",
    "ctb_5.1_dev": "ctb_5.1/dev.gold.stripped",
    "ctb_5.1_test": "ctb_5.1/test.gold.stripped",
    "ctb_5.1_train": "ctb_5.1/train.gold.stripped",
}
CORPORA_FILES = {k: os.path.join(BASE_PATH, v) for k,v in CORPORA_FILES.items()}

CHINESE_CORPORA_NAMES = list(sorted(k for k in CORPORA_FILES if k.startswith("ctb_")))
ENGLISH_CORPORA_NAMES = list(sorted(k for k in CORPORA_FILES if not k.startswith("ctb_")))

BROWN_CORPORA_NAMES = list(sorted(k for k in CORPORA_FILES if k.startswith("brown_")))
WSJ_CORPORA_NAMES = list(sorted(k for k in CORPORA_FILES if k.startswith("wsj_")))
EWT_CORPORA_NAMES = list(sorted(k for k in CORPORA_FILES if k.startswith("ewt_")))
GENIA_CORPORA_NAMES = list(sorted(k for k in CORPORA_FILES if k.startswith("genia_")))
CTB5_CORPORA_FILES = list(sorted(k for k in CORPORA_FILES if k.startswith("ctb_5.1")))
CTB9_CORPORA_NAMES = list(sorted(k for k in CORPORA_FILES if k.startswith("ctb_9.0")))

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
    'brown_all': 'Brown (all)',

    'genia_train': 'Genia (train)',
    'genia_dev': 'Genia (dev)',
    'genia_test': 'Genia (test)',
    'genia_all': 'Genia (all)',

    'wsj_train': 'WSJ (train)',
    'wsj_dev': 'WSJ (dev)',
    'wsj_test': 'WSJ (test)',

    'wsj_test_sim': 'WSJ (test) - similar',
    'wsj_test_dis': 'WSJ (test) - dissimilar',
    'wsj_test_v0g0': 'WSJ (test) - vocab 0 grammar 0',
    'wsj_test_v0g1': 'WSJ (test) - vocab 0 grammar 1',
    'wsj_test_v1g0': 'WSJ (test) - vocab 1 grammar 0',
    'wsj_test_v1g1': 'WSJ (test) - vocab 1 grammar 1',
    'wsj_test_mwp_dis': 'WSJ (test) - dissimilar MWP',
    'wsj_test_mwp_sim': 'WSJ (test) - similar MWP',
    'wsj_test_vocab_dis': 'WSJ (test) - dissimilar vocab',
    'wsj_test_vocab_sim': 'WSJ (test) - similar vocab',

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
    'ewt_all': 'EWT all',

    "ctb_9.0_broadcast_conversations": "CTB 9.0 Broadcast Conversations",
    "ctb_9.0_broadcast_news": "CTB 9.0 Broadcast News",
    "ctb_9.0_chat_messages": "CTB 9.0 Chat Messages",
    "ctb_9.0_conversational_speech": "CTB 9.0 Conversational Speech",
    "ctb_9.0_discussion_forums": "CTB 9.0 Discussion Forums",
    "ctb_9.0_newswire": "CTB 9.0 Newswire",
    "ctb_9.0_weblogs": "CTB 9.0 Weblogs",

    "ctb_5.1_dev": "CTB 5.1 (dev)",
    "ctb_5.1_test": "CTB 5.1 (test)",
    "ctb_5.1_train": "CTB 5.1 (train)",
}

CORPORA_SHORT_NAMES = {
    'brown': 'Brown All',
    'brown_cf': 'Brown CF',
    'brown_cg': 'Brown CG',
    'brown_ck': 'Brown CK',
    'brown_cl': 'Brown CL',
    'brown_cm': 'Brown CM',
    'brown_cn': 'Brown CN',
    'brown_cp': 'Brown CP',
    'brown_cr': 'Brown CR',

    'brown_train': 'Brown Train',
    'brown_test': 'Brown Test',
    'brown_test40': 'Brown Test40',
    'brown_all': 'Brown All',

    'genia_train': 'Genia Train',
    'genia_dev': 'Genia Dev',
    'genia_test': 'Genia Test',
    'genia_all': 'Genia All',

    'wsj_train': 'WSJ Train',
    'wsj_dev': 'WSJ Dev',
    'wsj_test': 'WSJ Test',

    'wsj_test_sim': 'WSJ Test Sim',
    'wsj_test_dis': 'WSJ Test Dissim',
    'wsj_test_v0g0': 'WSJ Test V0G0',
    'wsj_test_v0g1': 'WSJ Test V0G1',
    'wsj_test_v1g0': 'WSJ Test V1G0',
    'wsj_test_v1g1': 'WSJ Test V1G1',
    'wsj_test_mwp_dis': 'WSJ Test Dis MWP',
    'wsj_test_mwp_sim': 'WSJ Test Sim MWP',
    'wsj_test_vocab_dis': 'WSJ Test Dis Vocab',
    'wsj_test_vocab_sim': 'WSJ Test Sim Vocab',

    'ewt_answers_dev': 'EWT AD',
    'ewt_answers_test': 'EWT AT',
    'ewt_email_dev': 'EWT ED',
    'ewt_email_test': 'EWT ET',
    'ewt_newsgroup_dev': 'EWT ND',
    'ewt_newsgroup_test': 'EWT NT',
    'ewt_reviews_dev': 'EWT RD',
    'ewt_reviews_test': 'EWT RT',
    'ewt_weblog_dev': 'EWT WD',
    'ewt_weblog_test': 'EWT WT',
    'ewt_all': 'EWT All',

    "ctb_9.0_broadcast_conversations": "9.0 BC",
    "ctb_9.0_broadcast_news": "9.0 BN",
    "ctb_9.0_chat_messages": "9.0 CM",
    "ctb_9.0_conversational_speech": "9.0 CS",
    "ctb_9.0_discussion_forums": "9.0 DF",
    "ctb_9.0_newswire": "9.0 NW",
    "ctb_9.0_weblogs": "9.0 W",

    "ctb_5.1_dev": "5.1 Dev",
    "ctb_5.1_test": "5.1 Test",
    "ctb_5.1_train": "5.1 Train",
}

DECODE_NAME_NORM = {
}

DECODE_NAME_UNNORM = {
}

for corpus in CORPORA_FILES:
    if corpus.startswith("ctb"):
        replaced = corpus.replace("ctb_5.1_", "ctb_5.1-")
        replaced = replaced.replace("ctb_9.0_", "ctb_9.0-")
    else:
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
