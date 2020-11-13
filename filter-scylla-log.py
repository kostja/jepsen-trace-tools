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
    return re.match(r".*scylla:  \[shard", line)

def prettify(line, key):
    m = re.findall(r"^\d\d\d\d-\d\d-\d\dT\d\d:(\d\d\:\d\d\.\d+)\+\d\d:\d\d (\w+) scylla:  \[shard 0\] (.*)$", line)
    if not m:
        return ''
    time, shard, l = m[0]
    return l + "\n"

def process(f, args):
    while True:
        l = f.readline()
        if not l:
            break
        if match(l, args.key):
            try:
                sys.stdout.write(prettify(l, args.key))
            except BrokenPipeError:
                break

def main():
    args = parse_cmd_line()
    if args.path:
        with open(args.path[0], "r") as f:
            process(f, args)
    else:
        process(sys.stdin, args)

if __name__ == "__main__":
    main()
