#!/usr/bin/env python3
import argparse
import re
import sys

def parse_cmd_line():
    parser = argparse.ArgumentParser(description="history.edn filter")

    parser.add_argument(
        "path",
        nargs = "*",
        action="store",
        help="""Path to history.edn""")

    parser.add_argument(
        '--key', '-k', action="store",
        default="1", type=str,
        help="The key to look for")

    args = parser.parse_args()
    return args

def match(line, key):
    return True

def prettify(line, key):
    return re.sub(r"^\d\d\d\d-\d\d-\d\dT\d\d:(\d\d\:\d\d\.\d+)\+\d\d:\d\d (.*)$", r"\1 \2", line)

def process(f, args):
    while True:
        l = f.readline()
        if not l:
            break
        if match(l, args.key):
            sys.stdout.write(prettify(l, args.key))

def main():
    args = parse_cmd_line()
    if args.path:
        with open(args.path[0], "r") as f:
            process(f, args)
    else:
        process(sys.stdin, args)

if __name__ == "__main__":
    main()
