#!/usr/bin/env python

import sys


from rpython.rlib.streamio import open_file_as_stream


import kermit
from kermit.interpreter import interpret


USAGE = "kermit <filename>"
VERSION = "kermit v" + kermit.__version__


class Options(object):

    """Options Object Container"""


def parse_bool_arg(name, argv):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del(argv[i])
            return True
    return False


def parse_arg(name, argv):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del(argv[i])
            return argv.pop(i)
    return ""


def parse_args(argv):
    opts = Options()

    opts.help = parse_bool_arg("--help", argv)
    opts.version = parse_bool_arg("--version", argv)

    if opts.help:
        print USAGE
        raise SystemExit(0)

    if opts.version:
        print VERSION
        raise SystemExit(0)

    del argv[0]

    if not argv:
        print USAGE
        raise SystemExit(1)

    return opts, argv


def main(argv):
    try:
        opts, files = parse_args(argv)

        return run(files, opts)
    except SystemExit:
        return 0


def run(files, opts):
    for file in files:
        f = open_file_as_stream(file)
        data = f.readall()
        f.close()
        interpret(data)

    return 0


def entrypoint():
    """setuptools Entry Point"""

    return main(sys.argv)


if __name__ == "__main__":  # pragma: no cover
    entrypoint()
