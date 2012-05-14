
from kermit.sourceparser import parse
from kermit.bytecode import compile_ast
from kermit import bytecode
from pypy.rlib import jit

driver = jit.JitDriver(greens = ['pc', 'code', 'bc'], reds = ['frame'],
                       virtualizables=['frame'])

class W_Root(object):
    pass

class W_IntObject(W_Root):
    def __init__(self, intval):
        self.intval

    def add(self, other):
        if not isinstance(other, W_IntObject):
            raise Exception("wrong type")
        return W_IntObject(self.intval + other.intval)

class W_FloatObject(W_Root):
    def __init__(self, floatval):
        self.floatval


class Frame(object):
    _virtualizable2_ = ['valuestack[*]', 'valuestack_pos']
    
    def __init__(self, bc):
        self.valuestack = [0] * 100 # safe estimate!
        self.vars = [0] * bc.numvars
        self.valuestack_pos = 0

    def push(self, v):
        pos = self.valuestack_pos
        assert pos >= 0
        self.valuestack[pos] = v
        self.valuestack_pos = pos + 1
    
    def pop(self):
        new_pos = self.valuestack_pos - 1
        assert new_pos >= 0
        v = self.valuestack[new_pos]
        self.valuestack_pos = new_pos
        return v

def add(left, right):
    return left + right

def execute(frame, bc):
    code = bc.code
    pc = 0
    while True:
        driver.jit_merge_point(pc=pc, code=code, bc=bc, frame=frame)
        c = ord(code[pc])
        arg = ord(code[pc + 1])
        pc += 2
        if c == bytecode.LOAD_CONSTANT:
            frame.push(bc.constants[arg])
        elif c == bytecode.DISCARD_TOP:
            frame.pop()
        elif c == bytecode.RETURN:
            return
        elif c == bytecode.BINARY_ADD:
            right = frame.pop()
            left = frame.pop()
            frame.push(add(left, right))
        elif c == bytecode.BINARY_LT:
            right = frame.pop()
            left = frame.pop()
            frame.push(left < right)
        elif c == bytecode.JUMP_IF_FALSE:
            if not frame.pop():
                pc = arg
        elif c == bytecode.JUMP_BACKWARD:
            pc = arg
        elif c == bytecode.PRINT:
            item = frame.pop()
            print item
        elif c == bytecode.ASSIGN:
            frame.vars[arg] = frame.pop()
        elif c == bytecode.LOAD_VAR:
            frame.push(frame.vars[arg])
        else:
            assert False

def interpret(source):
    bc = compile_ast(parse(source))
    frame = Frame(bc)
    execute(frame, bc)
    return frame # for tests and later introspection
