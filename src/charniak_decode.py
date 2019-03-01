import subprocess
from load_corpora import CORPORA_FILES, DECODE_NAME_NORM
import os.path

def call_bllip(input_corpus_file, output_corpus_file, bllip_path):
    input_corpus_file = os.path.abspath(input_corpus_file)
    output_corpus_file = os.path.abspath(output_corpus_file)

    command = "second-stage/programs/prepare-data/ptb -c {} | ./parse.sh -K > {}".format(input_corpus_file, output_corpus_file)
    print(command)

    out = subprocess.run(command, cwd=bllip_path, shell=True, stderr=subprocess.PIPE)
    out_dec = out.stderr.decode('utf-8')
    if out_dec.strip():
        print(out_dec)

def retag(input_corpus_file, pred_file, retagged_file):
    command = 'python ../scripts/retag.py {} {} > {}'.format(input_corpus_file, pred_file, retagged_file)
    print(command)

    out = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    out_dec = out.stderr.decode('utf-8')
    if out_dec.strip():
        print(out_dec)

def output_fname(corpus_name, suffix):
    return "{}-charniak_{}.test.txt".format(DECODE_NAME_NORM[corpus_name], suffix)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpora", nargs="*")
    parser.add_argument("--bllip_root", default='../../bllip-parser')
    parser.add_argument("--decode_output_folder", default='../decodes')

    args = parser.parse_args()

    corpora = args.corpora

    if not corpora:
        corpora = CORPORA_FILES.keys()

    for corpus in corpora:
        print("corpus: {}".format(corpus))
        gold_file = CORPORA_FILES[corpus]
        pred_file = os.path.join(args.decode_output_folder, output_fname(corpus, "pred"))
        retag_file = os.path.join(args.decode_output_folder, output_fname(corpus, "pred-tag-replaced"))

        call_bllip(gold_file, pred_file, args.bllip_root)
        retag(gold_file, pred_file, retag_file)
