import sys
sys.path.append("../scripts")
from remove_dev_unk import get_tags_tokens_lowercase
import subprocess
from load_corpora import ENGLISH_CORPORA_NAMES, DECODE_NAME_NORM, CORPORA_FILES
import os.path
import tqdm
from bllipparser import RerankingParser

def parse(parser, name, input_corpus_file, output_corpus_file, no_rerank):
    sentences = []
    with open(input_corpus_file) as f:
        for line in f:
            sentences.append(get_tags_tokens_lowercase(line.strip())[1])

    parses = []
    with open(output_corpus_file, 'w') as f:
        for i, sent in tqdm.tqdm(list(enumerate(sentences)), desc=name, ncols=80):
            try:
                parsed = parser.parse(sent)
                if no_rerank:
                    parse = str(parsed.get_parser_best().ptb_parse)
                else:
                    parse = str(parsed.get_reranker_best().ptb_parse)
                assert parse.startswith("(S1 ")
                parse = "(TOP " + parse[4:]
                parses.append(parse)
                f.write("{}\n".format(parse))
            except Exception as e:
                print('exception on sent {}'.format(i))
                print(e)
                f.write("\n")

def retag(input_corpus_file, pred_file, retagged_file):
    command = 'python ../scripts/retag.py {} {} > {}'.format(input_corpus_file, pred_file, retagged_file)
    print(command)

    out = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    out_dec = out.stderr.decode('utf-8')
    if out_dec.strip():
        print(out_dec)

def output_fname(corpus_name, parser_model, no_rerank, suffix):
    model = "charniak-{}".format(parser_model)
    if no_rerank:
        model += "-no-rerank"
    return "{}-{}_{}.test.txt".format(DECODE_NAME_NORM[corpus_name], model, suffix)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpora", nargs="*", default=ENGLISH_CORPORA_NAMES)
    parser.add_argument("--decode_output_folder", default='../decodes')
    parser.add_argument("--parser_model", default='WSJ-PTB3')
    parser.add_argument("--no_rerank", action='store_true')

    args = parser.parse_args()

    parser = RerankingParser.fetch_and_load(args.parser_model)

    for corpus in args.corpora:
        print("corpus: {}".format(corpus))
        gold_file = CORPORA_FILES[corpus]
        pred_file = os.path.join(args.decode_output_folder, output_fname(corpus, args.parser_model, args.no_rerank, "pred"))
        retag_file = os.path.join(args.decode_output_folder, output_fname(corpus, args.parser_model, args.no_rerank, "pred-tag-replaced"))

        parse(parser, corpus, gold_file, pred_file, args.no_rerank)
        retag(gold_file, pred_file, retag_file)
