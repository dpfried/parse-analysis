import math
import shutil
import os.path
import re
import subprocess
import tempfile

import trees

import collections

class SentenceScore(object):
    def __init__(self,
            length, skip,
            recall, precision, matched_bracket, gold_bracket, guess_bracket, cross_bracket,
            words, correct_tags, tagging_accuracy
            ):
        self.length = int(length)
        self.skip = bool(skip)
        self.recall = float(recall)
        self.precision = float(precision)
        self.matched_bracket = int(matched_bracket)
        self.gold_bracket = int(gold_bracket)
        self.guess_bracket = int(guess_bracket)
        self.cross_bracket = int(cross_bracket)
        self.words = int(words)
        self.correct_tags = int(correct_tags)
        self.tagging_accuracy = float(tagging_accuracy)

    def __str__(self):
        return "(MatchedBracket={:.2f}, GoldBracket={:.2f}, GuessBracket={:.2f})".format(
            self.matched_bracket, self.gold_bracket, self.guess_bracket)

class FScore(object):
    def __init__(self,
            recall,
            precision,
            fscore,
            complete_match,
            sentence_scores=None,
            tagging_accuracy=100,
            ):
        self.recall = recall
        self.precision = precision
        self.fscore = fscore
        self.complete_match = complete_match
        self.sentence_scores = sentence_scores
        self.tagging_accuracy = tagging_accuracy

    def __str__(self):
        if self.tagging_accuracy < 100:
            return "(Recall={:.2f}, Precision={:.2f}, FScore={:.2f}, CompleteMatch={:.2f}, TaggingAccuracy={:.2f})".format(
                self.recall, self.precision, self.fscore, self.complete_match, self.tagging_accuracy)
        else:
            return "(Recall={:.2f}, Precision={:.2f}, FScore={:.2f}, CompleteMatch={:.2f})".format(
                self.recall, self.precision, self.fscore, self.complete_match)

InvalidCounts = collections.namedtuple("InvalidCounts", ["error_sentence_count", "skip_sentence_count"])

INT = "(\d+)"
FLOAT = "(\d+\.\d+)"
SEP = "\s+"
EVALB_PATTERN = f"\s*{INT}{SEP}{INT}{SEP}{INT}{SEP}{FLOAT}{SEP}{FLOAT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{FLOAT}"

def evalb_from_trees(gold_trees, predicted_trees, evalb_dir=None, ref_gold_path=None, abort_on_error_or_skip=False):
    assert len(gold_trees) == len(predicted_trees)
    for gold_tree, predicted_tree in zip(gold_trees, predicted_trees):
        assert isinstance(gold_tree, trees.TreebankNode)
        assert isinstance(predicted_tree, trees.TreebankNode)
        gold_leaves = list(gold_tree.leaves())
        predicted_leaves = list(predicted_tree.leaves())
        assert len(gold_leaves) == len(predicted_leaves)
        assert all(
            gold_leaf.word == predicted_leaf.word
            for gold_leaf, predicted_leaf in zip(gold_leaves, predicted_leaves))

    temp_dir = tempfile.mkdtemp(prefix="evalb-")
    gold_path = os.path.join(temp_dir, "gold.txt")
    predicted_path = os.path.join(temp_dir, "predicted.txt")
    output_path = os.path.join(temp_dir, "output.txt")

    with open(gold_path, "w") as outfile:
        if ref_gold_path is None:
            for tree in gold_trees:
                outfile.write("{}\n".format(tree.linearize()))
        else:
            # For the SPMRL dataset our data loader performs some modifications
            # (like stripping morphological features), so we compare to the
            # raw gold file to be certain that we haven't spoiled the evaluation
            # in some way.
            with open(ref_gold_path) as goldfile:
                outfile.write(goldfile.read())

    with open(predicted_path, "w") as outfile:
        for tree in predicted_trees:
            outfile.write("{}\n".format(tree.linearize()))

    tree_count = max(len(gold_trees), len(predicted_trees))

    fscore, invalid_counts, read_and_valid = evalb_from_files(
        predicted_path, gold_path, output_path,
        evalb_dir=evalb_dir, abort_on_error_or_skip=abort_on_error_or_skip, tree_count=tree_count
    )

    if read_and_valid:
        shutil.rmtree(temp_dir)
    return fscore


def evalb_from_files(predicted_path, gold_path, output_path=None, evalb_dir=None, abort_on_error_or_skip=False, tree_count=None):
    if evalb_dir is None:
        evalb_dir = os.path.join(os.path.dirname(__file__), '../EVALB')

    if output_path is None:
        temp_dir = tempfile.mkdtemp(prefix="evalb-")
        output_path = os.path.join(temp_dir, "output.txt")
    else:
        temp_dir = None

    assert os.path.exists(evalb_dir)
    evalb_program_path = os.path.join(evalb_dir, "evalb")
    evalb_spmrl_program_path = os.path.join(evalb_dir, "evalb_spmrl")
    assert os.path.exists(evalb_program_path) or os.path.exists(evalb_spmrl_program_path)

    if os.path.exists(evalb_program_path):
        evalb_param_path = os.path.join(evalb_dir, "COLLINS_ch.prm")
    else:
        evalb_program_path = evalb_spmrl_program_path
        evalb_param_path = os.path.join(evalb_dir, "spmrl.prm")

    assert os.path.exists(evalb_program_path)
    assert os.path.exists(evalb_param_path)

    sentence_scores = [None for _ in range(tree_count)] if tree_count is not None else []
    fscore = FScore(
        math.nan, math.nan, math.nan, math.nan,
        sentence_scores=sentence_scores,
    )

    invalid_counts = InvalidCounts(None, None)

    if not os.path.exists(predicted_path):
        print("Test file {} does not exist!".format(predicted_path))
        return fscore, invalid_counts, False

    command = "{} -p {} {} {} > {}".format(
        evalb_program_path,
        evalb_param_path,
        gold_path,
        predicted_path,
        output_path,
    )
    out = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    stderr_dec = out.stderr.decode("utf-8")
    if stderr_dec.strip():
        print(stderr_dec.strip())

    with open(output_path) as infile:
        for line in infile:
            match = re.match(EVALB_PATTERN, line.strip())
            if match:
                sent_id, *stats = match.groups()
                if tree_count is None:
                    fscore.sentence_scores.append(SentenceScore(*stats))
                else:
                    fscore.sentence_scores[int(sent_id) - 1] = SentenceScore(*stats)
            match = re.match(r"Number of Error sentence\s+=\s+(\d+)", line)
            if match:
                invalid_counts = invalid_counts._replace(error_sentence_count=int(match.group(1)))
            match = re.match(r"Number of Skip  sentence\s+=\s+(\d+)", line)
            if match:
                invalid_counts = invalid_counts._replace(skip_sentence_count=int(match.group(1)))
            # match = re.match(r"Number of Valid sentence\s+=\s+(\d+)", line)
            # if match:
            #     valid_sentence = int(match.group(1))

            match = re.match(r"Bracketing Recall\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.recall = float(match.group(1))
            match = re.match(r"Bracketing Precision\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.precision = float(match.group(1))
            match = re.match(r"Bracketing FMeasure\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.fscore = float(match.group(1))
            match = re.match(r"Complete match\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.complete_match = float(match.group(1))
            match = re.match(r"Tagging accuracy\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.tagging_accuracy = float(match.group(1))
                break

    read_results = (
        not math.isnan(fscore.fscore) or
        fscore.recall == 0.0 or
        fscore.precision == 0.0)

    valid = True
    if (invalid_counts.error_sentence_count is None or invalid_counts.error_sentence_count > 0):
        print("{} Error sentences".format(invalid_counts.error_sentence_count))
        valid = False
        if abort_on_error_or_skip:
            raise Exception("{} Error sentences".format(invalid_counts.error_sentence_count))

    if (invalid_counts.skip_sentence_count is None or invalid_counts.skip_sentence_count > 0):
        print("{} Skip sentences".format(invalid_counts.skip_sentence_count))
        valid = False
        if abort_on_error_or_skip:
            raise Exception("{} Error sentences".format(invalid_counts.skip_sentence_count))

    if not read_results:
        print("Error reading EVALB results.")

    read_and_valid = (read_results and valid)
    if not read_and_valid:
        print("Gold path: {}".format(gold_path))
        print("Predicted path: {}".format(predicted_path))
        print("Output path: {}".format(output_path))

    if temp_dir and read_and_valid:
        shutil.rmtree(temp_dir)

    return fscore, invalid_counts, read_and_valid
