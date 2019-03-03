import sys
sys.path.append("../scripts")
from strip_functional import PhraseTree
import subprocess
from load_corpora import CHINESE_CORPORA_NAMES, DECODE_NAME_NORM, CORPORA_FILES
import os.path
import tempfile
from zpar_decode import dump_tagged_tokens

from charniak_python_decode import retag

def parse(berkeley_root, input_file, output_file):
    input_file = os.path.abspath(input_file)
    output_file = os.path.abspath(output_file)

    command = "java -jar BerkeleyParser-1.7.jar -gr eng_sm6.gr < {} > {}".format(input_file, output_file)

    out = subprocess.run(command, cwd=berkeley_root, shell=True, stderr=subprocess.PIPE)
    out_dec = out.stderr.decode('utf-8')
    if out_dec.strip():
        print(out_dec)

def add_top(pred_raw_file, pred_top_file):
    with open(pred_raw_file) as f_in, open(pred_contract_file, 'w') as f_out:
        for i, line in enumerate(f_in):
            line = line.rstrip()
            if not line.startswith("( "):
                print("line {}: {}".format(i, line.rstrip()))
            else:
                line = "(TOP " + line[2:]
            f_out.write("{}\n".format(line))

def output_fname(corpus_name, suffix):
    parser_name = 'berkeley-sm6'

    return "{}-{}_{}.test.txt".format(DECODE_NAME_NORM[corpus_name], parser_name, suffix)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpora", nargs="*", default=CHINESE_CORPORA_NAMES)
    parser.add_argument("--decode_output_folder", default='../decodes')
    parser.add_argument("--berkeley_root", default='../../berkeleyparser')

    args = parser.parse_args()

    for corpus in args.corpora:
        print("corpus: {}".format(corpus))
        gold_file = CORPORA_FILES[corpus]
        gold_tok_f, gold_tok_file = tempfile.mkstemp()
        dump_tagged_tokens(gold_file, gold_tok_file, dump_tags=False)

        pred_raw_file = os.path.join(args.decode_output_folder, output_fname(corpus, "pred-raw"))
        parse(args.berkeley_root, gold_tok_file, pred_raw_file)

        pred_contract_file = os.path.join(args.decode_output_folder, output_fname(corpus, "pred"))
        add_top(pred_raw_file, pred_contract_file)

        retag_file = os.path.join(args.decode_output_folder, output_fname(corpus, "pred-tag-replaced"))
        retag(gold_file, pred_contract_file, retag_file)
