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
    args = parser.parse_args()
    return args

def match(line):
    if re.search(":append 1 ", line):
        return True
    if re.search(":r 1 ", line):
        return True
    if re.search(":r \d+ ", line):
        return False
    if re.search(":append \d+ ", line):
        return False
    return True

def main():
    args = parse_cmd_line()
    with open(args.path[0], "r") as f:
        while True:
            l = f.readline()
            if not l:
                break
            if match(l):
                sys.stdout.write(l)

if __name__ == "__main__":
    main()
