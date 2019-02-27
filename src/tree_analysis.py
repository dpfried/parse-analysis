import subprocess
from load_corpora import CORPORA_FILES, DECODE_NAME_NORM
import os.path
import parsers

def call_analysis(gold_file, pred_file, output_prefix, analysis_path='../../berkeley-parser-analyser'):

    classify = os.path.join(analysis_path, 'berkeley_parse_analyser', 'classify_english.py')

    command = "python3 ../scripts/ensure_top.py < {} | python2 {} {} - {}".format(
        pred_file, classify, gold_file, output_prefix
    )
    print(command)

    out = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    out_dec = out.stderr.decode('utf-8')
    if out_dec.strip():
        print(out_dec)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpora", nargs="*")
    parser.add_argument("--model_names", nargs="*")
    parser.add_argument("--analysis_root", default='../../berkeley-parser-analyser')
    parser.add_argument("--decodes_folder", default='../decodes')
    parser.add_argument("--analysis_output_folder", default='../decode_analysis')

    args = parser.parse_args()

    corpora = args.corpora

    if not corpora:
        corpora = CORPORA_FILES.keys()

    model_names = args.model_names
    if not model_names:
        model_names = [model['name'] for model in parsers.ALL_MODELS]

    for corpus in corpora:
        for model_name in model_names:
            print()
            print("{} {}".format(corpus, model_name))
            pred_file = parsers.get_predicted_file(DECODE_NAME_NORM[corpus], model_name, args.decodes_folder)
            if not os.path.exists(pred_file):
                print("no decode found for {}".format(pred_file))
                continue
            output_prefix = os.path.join(args.analysis_output_folder, "{}-{}".format(DECODE_NAME_NORM[corpus], model_name))
            print("output to {}".format(output_prefix))

            call_analysis(CORPORA_FILES[corpus], pred_file, output_prefix)
