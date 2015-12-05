
"""This file contains both an interpreter and "hints" in the interpreter code
necessary to construct a Jit.

There are two required hints:
1. JitDriver.jit_merge_point() at the start of the opcode dispatch loop
2. JitDriver.can_enter_jit() at the end of loops
   (where they jump back to the start)

These bounds and the "green" variables effectively mark loops and
allow the jit to decide if a loop is "hot" and in need of compiling.

Read http://doc.pypy.org/en/latest/jit/pyjitpl5.html for details.

"""


from rpython.rlib import jit
from rpython.rlib.streamio import open_file_as_stream


import kermit
from kermit import bytecode
from kermit.parser import parse
from kermit.compiler import Compiler
from kermit.rreadline import readline


BANNER = "%s %s\n" % (kermit.__name__, kermit.__version__)
PS1 = ">>> "
PS2 = "... "


def printable_loc(pc, code, *_):
    """Return a printable source location for JIT Debugging

    :param _: bc (unused)

    .. note:: All green parameters are passed in-order.
    """

    return str(pc) + " " + bytecode.bytecodes[ord(code[pc])]


driver = jit.JitDriver(
   greens=['pc', 'code', 'bc'],
   reds=['frame', 'self'],
   virtualizables=['frame'],
   get_printable_location=printable_loc
)


class Frame(object):
    _virtualizable_ = ['valuestack[*]', 'valuestack_pos', 'vars[*]']

    def __init__(self):
        self = jit.hint(self, fresh_virtualizable=True, access_directly=True)
        self.valuestack = [None] * 3  # safe estimate!
        self.vars = [None] * 1024  # safe estimate!
        self.valuestack_pos = 0

    def push(self, v):
        pos = jit.hint(self.valuestack_pos, promote=True)
        assert pos >= 0
        self.valuestack[pos] = v
        self.valuestack_pos = pos + 1

    def pop(self):
        pos = jit.hint(self.valuestack_pos, promote=True)
        new_pos = pos - 1
        assert new_pos >= 0
        v = self.valuestack[new_pos]
        self.valuestack_pos = new_pos
        return v


class Interpreter(object):

    def __init__(self, debug=False, banner=BANNER, ps1=PS1, ps2=PS2):
        self.debug = debug
        self.banner = banner
        self.ps1 = ps1
        self.ps2 = ps2

        self.frame = Frame()
        self.compiler = Compiler()

    def runstring(self, s):
        ast = parse(s)

        bc = self.compiler.compile(ast)
        if self.debug:
            print bc.dump()

        return self.run(bc)

    def runfile(self, filename):
        f = open_file_as_stream(filename)
        s = f.readall()
        f.close()

        return self.runstring(s)

    def repl(self, banner=None, ps1=None, ps2=None):
        banner = banner or self.banner
        ps1 = ps1 or self.ps1
        ps2 = ps2 or self.ps2

        print banner

        while True:
            try:
                s = readline(ps1).strip()
            except EOFError:
                break

            self.runstring(s)

    def run(self, bc):  # noqa
        frame = self.frame
        code = bc.code
        pc = 0

        while True:
            # required hint indicating this is the top of the opcode dispatch
            driver.jit_merge_point(
               pc=pc, code=code, bc=bc, frame=frame, self=self
            )

            c = ord(code[pc])
            arg = ord(code[pc + 1])
            pc += 2

            if c == bytecode.LOAD_CONSTANT:
                w_constant = bc.constants[arg]
                frame.push(w_constant)
            elif c == bytecode.LOAD_STRING:
                w_constant = bc.strconstants[arg]
                frame.push(w_constant)
            elif c == bytecode.DISCARD_TOP:
                frame.pop()
            elif c == bytecode.RETURN:
                return
            elif c == bytecode.BINARY_ADD:
                right = frame.pop()
                left = frame.pop()
                w_res = left.add(right)
                frame.push(w_res)
            elif c == bytecode.BINARY_LT:
                right = frame.pop()
                left = frame.pop()
                frame.push(left.lt(right))
            elif c == bytecode.JUMP_IF_FALSE:
                if not frame.pop().is_true():
                    pc = arg
            elif c == bytecode.JUMP_BACKWARD:
                pc = arg
                # required hint indicating this is the end of a loop
                driver.can_enter_jit(
                  pc=pc, code=code, bc=bc, frame=frame, self=self
               )
            elif c == bytecode.PRINT:
                item = frame.pop()
                print item.str()
            elif c == bytecode.ASSIGN:
                frame.vars[arg] = frame.pop()
            elif c == bytecode.LOAD_VAR:
                frame.push(frame.vars[arg])
            elif c == bytecode.LOAD_FUNC:
                w_function = bc.functions[arg]
                frame.push(w_function)
            elif c == bytecode.CALL:
                w_function = frame.pop()
                frame.push(self.run(w_function.bc))
            else:
                raise Exception("illegal instruction")


def interpret(source):
    return Interpreter().run(Compiler().compile(parse(source)))
