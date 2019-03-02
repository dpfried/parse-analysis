import sys
sys.path.append("../scripts")
from strip_functional import PhraseTree
import subprocess
from load_corpora import CHINESE_CORPORA_NAMES, DECODE_NAME_NORM, CORPORA_FILES
import os.path
import tempfile

from charniak_python_decode import retag

def dump_tagged_tokens(input_corpus_file, temp_file, dump_tags=False):
    with open(input_corpus_file) as f_in, open(temp_file, 'w') as f_out:
        for line in f_in:
            tree = PhraseTree.parse(line.rstrip())
            toks = []
            for pair in tree.sentence:
                if dump_tags:
                    toks.append("{}_{}".format(pair[0], pair[1]))
                else:
                    toks.append(pair[0])
            f_out.write("{}\n".format(' '.join(toks)))

def parse(zpar_root, input_file, output_file, use_external_tags):
    input_file = os.path.abspath(input_file)
    output_file = os.path.abspath(output_file)

    command = "dist/chinese.conparser/conparser {} {} chinese-models/conparser -m{}".format(
        input_file, output_file, 2 if use_external_tags else 1
    )
    print(command)

    out = subprocess.run(command, cwd=zpar_root, shell=True, stderr=subprocess.PIPE)
    out_dec = out.stderr.decode('utf-8')
    if out_dec.strip():
        print(out_dec)

def contract(pred_raw_file, pred_contract_file):
    with open(pred_raw_file) as f_in, open(pred_contract_file, 'w') as f_out:
        for line in f_in:
            tree = PhraseTree.parse(line.rstrip())
            contracted = tree.zpar_contract()
            f_out.write("{}\n".format(contracted))

def output_fname(corpus_name, use_external_tags, suffix):
    parser_name = 'zpar-exttags' if use_external_tags else 'zpar'

    return "{}-{}_{}.test.txt".format(DECODE_NAME_NORM[corpus_name], parser_name, suffix)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpora", nargs="*", default=CHINESE_CORPORA_NAMES)
    parser.add_argument("--decode_output_folder", default='../decodes')
    parser.add_argument("--zpar_root", default='../../zpar')
    parser.add_argument("--use_external_tags", action='store_true', help='not recommended')

    args = parser.parse_args()

    for corpus in args.corpora:
        print("corpus: {}".format(corpus))
        gold_file = CORPORA_FILES[corpus]
        gold_tok_f, gold_tok_file = tempfile.mkstemp()
        dump_tagged_tokens(gold_file, gold_tok_file, dump_tags=args.use_external_tags)

        pred_raw_file = os.path.join(args.decode_output_folder, output_fname(corpus, args.use_external_tags, "pred-raw"))
        parse(args.zpar_root, gold_tok_file, pred_raw_file, use_external_tags=args.use_external_tags)

        pred_contract_file = os.path.join(args.decode_output_folder, output_fname(corpus, args.use_external_tags, "pred"))
        contract(pred_raw_file, pred_contract_file)

        retag_file = os.path.join(args.decode_output_folder, output_fname(corpus, args.use_external_tags, "pred-tag-replaced"))
        retag(gold_file, pred_contract_file, retag_file)
