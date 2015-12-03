"""Main"""


import sys


from rpython.jit.codewriter.policy import JitPolicy
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
        _, args = parse_args(argv)

        filename = args[0]

        return run(filename)
    except SystemExit:
        return 0


def run(filename):
    f = open_file_as_stream(filename)
    source = f.readall()
    f.close()
    interpret(source)

    return 0


def entrypoint():
    return main(sys.argv)


def target(*dummy):
    """RPython Translation entrypoint

    :param driver: An instnace of a JITDriver
    :param args: argv
    """

    return main, None


def jitpolicy(*dummy):
    """JIT Policy

    :param driver: An instance of a JITDriver
    """

    return JitPolicy()
