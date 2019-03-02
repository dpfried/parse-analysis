import argparse
import fileinput
from strip_functional import PhraseTree

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    args = parser.parse_args()

    for line in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
        tree = PhraseTree.parse(line)
        print(tree.zpar_contract())
