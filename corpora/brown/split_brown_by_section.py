"""
Split Brown data into individual sections
"""

BROWN_SECTION_NAMES = ["cf", "cg", "ck", "cl", "cm", "cn", "cp", "cr"]
BROWN_SECTION_SIZES = [3164, 3279, 3881, 3714, 881, 4415, 3942, 967]

if __name__ == "__main__":
    import fileinput
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=BROWN_SECTION_NAMES, required=True)

    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    args = parser.parse_args()


    brown_section_starts = []
    brown_section_ends = []

    total = 0
    for size in BROWN_SECTION_SIZES:
        brown_section_starts.append(total)
        total += size
        brown_section_ends.append(total)

    section_id = BROWN_SECTION_NAMES.index(args.section)
    start = brown_section_starts[section_id]
    end = brown_section_ends[section_id]

    for i, line in enumerate(fileinput.input(files=args.files if len(args.files) > 0 else ('-', ))):
        if not line:
            continue
        if start <= i < end:
            print(line.strip())
