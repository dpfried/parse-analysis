"""
Partition Brown into train and test sets, following:
"Corpus Variation and Parser Performance" (Gildea, 2001)
"""

if __name__ == "__main__":
    import fileinput
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=['train', 'test', 'test40'], required=True)

    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    args = parser.parse_args()

    for i, line in enumerate(fileinput.input(files=args.files if len(args.files) > 0 else ('-', ))):
        if not line:
            continue

        split_for_line = 'test' if (i % 10 == 0) else 'train'
        if args.split == split_for_line:
            print(line.strip())
        elif args.split == 'test40' and split_for_line == 'test':
            num_tokens = len([x for x in [x.split(' ')[-1] for x in line.strip().split(')')] if x])
            if num_tokens <= 40:
                print(line.strip())
