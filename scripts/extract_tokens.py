import sys
import fileinput
from strip_functional import PhraseTree

def extract_tokens(line):
    tree = PhraseTree.parse(line.rstrip())
    return str(' '.join(["{}_{}".format(pair[0], pair[1]) for pair in tree.sentence]))
    #return str(' '.join(["{}".format(pair[0]) for pair in tree.sentence]))

def main():
    # use fileinput so we can pass "-" to read from stdin
    for line in fileinput.input(files=[sys.argv[1]]):
        print(extract_tokens(line))

if __name__ == '__main__':
    main()
