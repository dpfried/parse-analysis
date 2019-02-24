import sys
sys.path.append("../../scripts/")
import predict_tags
import os
import argparse

working_dir = "tag_prediction"

try:
    os.mkdir(working_dir)
except:
    pass

parser = argparse.ArgumentParser()
parser.add_argument("--splits", nargs="*")
parser.add_argument("--props_file", default="../ctb_5.1/jackknife/train-chinese-nodistsim.tagger.props")
parser.add_argument("--model_file", default="../ctb_5.1/jackknife/model_full.bin")

args = parser.parse_args()

input_files = ["{}.gold.stripped".format(split) for split in args.splits]
tag_files = [os.path.join(working_dir, "{}.pred.tags".format(split)) for split in args.splits]
output_files = ["{}.pred.stripped".format(split) for split in args.splits]
log_files = [os.path.join(working_dir, "{}.log".format(split)) for split in args.splits]

tag_replacement = {
    'NP': 'NN',
    'VP': 'VV',
    'X': 'FW',
}

predict_tags.run_partition(args.props_file, 
                           None, # train_file
                           input_files,
                           args.model_file,
                           None, # train_log_file
                           tag_files,
                           output_files, 
                           log_files,
                           args.splits,
                           train_models=False,
                           tag_replacement=tag_replacement)
