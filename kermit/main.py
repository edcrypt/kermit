"""Main"""


import sys


from rpython.jit.codewriter.policy import JitPolicy


import kermit
from kermit.rpath import basename
from kermit.interpreter import Interpreter


class Options(object):
    """Options Container"""


def usage(prog):
    print "Usage: %s [options] [file]" % prog
    return 0


def help():
    print "Options and Arguments:"
    print "  -d enable debug output"
    print "  -e evaluate the string"
    print "  -h display this help"
    print "  -i inspect interactively"
    print "  -v display the version"
    return 0


def version():
    print "%s %s" % (kermit.__name__, kermit.__version__)
    return 0


def parse_bool_arg(name, argv, default=False):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del argv[i]
            return True
    return default


def parse_arg(name, argv, default=""):
    for i in xrange(len(argv)):
        if argv[i] == name:
            del argv[i]
            return argv.pop(i)
    return default


def parse_args(argv):
    opts = Options()

    opts.debug = parse_bool_arg('-d', argv)
    opts.eval = parse_arg("-e", argv)
    opts.help = parse_bool_arg("-h", argv)
    opts.inspect = parse_bool_arg("-i", argv)
    opts.version = parse_bool_arg("-v", argv)

    del argv[0]

    return opts, argv


def main(argv):
    prog = basename(argv[0])
    opts, args = parse_args(argv)

    if opts.help:
        usage(prog)
        return help()

    if opts.version:
        return version()

    interpreter = Interpreter(debug=opts.debug)

    if args:
        interpreter.runfile(args[0])
        if opts.inspect:
            interpreter.repl()
    elif opts.eval:
        interpreter.runstring(opts.eval)
        if opts.inspect:
            interpreter.repl()
    else:
        interpreter.repl()

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
