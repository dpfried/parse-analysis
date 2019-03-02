import fileinput
import argparse

#!/usr/bin/env python

from strip_functional import PhraseTree

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_length', type=int, default=23)
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    args = parser.parse_args()

    for line in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
        line = line.strip()

        # line = re.sub('\)', ') ', line)

        # #line = re.sub(r'-[^\s^\)]* |##[^\s^\)]*## ', ' ', line)
        # #line = re.sub(r'##[^\s^\)]*## ', ' ', line)
        # tokens = line.split(' ')
        # proc_tokens = []
        # last_was_none = False
        # for tok in tokens:
        #     if last_was_none:
        #         # follows '(-NONE-', should just be a terminal that looks like *op*, drop it
        #         assert not '(' in tok
        #         assert '*' in tok
        #         assert tok.count(')') == 1 and tok[-1] == ')'
        #         last_was_none = False
        #         continue

        #     if tok.startswith('('):
        #         if '-NONE-' in tok:
        #             last_was_none = True
        #             continue
        #         # remove functional tags -- anything after a - but not preceeded by ##
        #         morph_split = tok.split('##')
        #         morph_split[0] = re.sub('-.*', '', morph_split[0])
        #         tok = '##'.join(morph_split)
        #     proc_tokens.append(tok)

        # linearized = ' '.join(proc_tokens)
        # linearized = re.sub('\) ', ')', linearized)
        # print(linearized)
        tree = PhraseTree.parse(line)
        if len(tree.sentence) > args.max_length:
            continue
        print(tree)
