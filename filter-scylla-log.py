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

re1 = re.compile(r".*scylla:  \[shard")

re2 = re.compile(r"^\d\d\d\d-\d\d-\d\dT\d\d:(\d\d\:\d\d\.\d+)\+\d\d:\d\d (\w+) scylla:  \[shard 0\] (.*)$")

re3 = r"(UPDATE(?:(?!UPDATE).)*AND id = {} IF lwt_trivial = null)"

re4 = r"(SELECT.*AND id = {});"

def match(line, key):
    return re1.match(line) and re.match(".*query_processor.*", line)

def prettify(line, key):
    m = re2.findall(line)
    if not m:
        return ''
    time, shard, l = m[0]
    m = re3.findall(l)
    if len(m):
        l = m[0]
        return "{} {} {}\n".format(time, shard, l)
    m = re4.findall(l)
    if len(m):
        l = m[0]
        return "{} {} {}\n".format(time, shard, l)
    return None

def process(f, args):
    while True:
        l = f.readline()
        if not l:
            break
        if match(l, args.key):
            try:
                l = prettify(l, args.key)
                if l:
                    sys.stdout.write(l)
            except BrokenPipeError:
                break

def main():
    args = parse_cmd_line()
    global re3
    global re4
    re3 = re.compile(re3.format(args.key))
    re4 = re.compile(re4.format(args.key))
    if args.path:
        with open(args.path[0], "r") as f:
            process(f, args)
    else:
        process(sys.stdin, args)

if __name__ == "__main__":
    main()
