import math
import os.path
import re
import subprocess
import tempfile

import trees

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

INT = "(\d+)"
FLOAT = "(\d+\.\d+)"
SEP = "\s+"
EVALB_PATTERN = f"\s*{INT}{SEP}{INT}{SEP}{INT}{SEP}{FLOAT}{SEP}{FLOAT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{INT}{SEP}{FLOAT}"

def evalb(gold_trees, predicted_trees, evalb_dir=None, ref_gold_path=None):
    if evalb_dir is None:
        evalb_dir = os.path.join(os.path.dirname(__file__), '../EVALB')

    assert os.path.exists(evalb_dir)
    evalb_program_path = os.path.join(evalb_dir, "evalb")
    evalb_spmrl_program_path = os.path.join(evalb_dir, "evalb_spmrl")
    assert os.path.exists(evalb_program_path) or os.path.exists(evalb_spmrl_program_path)

    if os.path.exists(evalb_program_path):
        evalb_param_path = os.path.join(evalb_dir, "COLLINS.prm")
    else:
        evalb_program_path = evalb_spmrl_program_path
        evalb_param_path = os.path.join(evalb_dir, "spmrl.prm")

    assert os.path.exists(evalb_program_path)
    assert os.path.exists(evalb_param_path)

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

    temp_dir = tempfile.TemporaryDirectory(prefix="evalb-")
    gold_path = os.path.join(temp_dir.name, "gold.txt")
    predicted_path = os.path.join(temp_dir.name, "predicted.txt")
    output_path = os.path.join(temp_dir.name, "output.txt")

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

    command = "{} -p {} {} {} > {}".format(
        evalb_program_path,
        evalb_param_path,
        gold_path,
        predicted_path,
        output_path,
    )
    subprocess.run(command, shell=True)

    fscore = FScore(
        math.nan, math.nan, math.nan, math.nan,
        sentence_scores=[None for _ in range(max(len(gold_trees), len(predicted_trees)))]
        )
    with open(output_path) as infile:
        for line in infile:
            match = re.match(EVALB_PATTERN, line.strip())
            if match:
                sent_id, *stats = match.groups()
                fscore.sentence_scores[int(sent_id) - 1] = SentenceScore(*stats)
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

    success = (
        not math.isnan(fscore.fscore) or
        fscore.recall == 0.0 or
        fscore.precision == 0.0)

    if success:
        temp_dir.cleanup()
    else:
        print("Error reading EVALB results.")
        print("Gold path: {}".format(gold_path))
        print("Predicted path: {}".format(predicted_path))
        print("Output path: {}".format(output_path))

    return fscore
