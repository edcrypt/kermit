
from kermit.sourceparser import parse
from kermit.bytecode import compile_ast
from kermit import bytecode
from rpython.rlib import jit

def printable_loc(pc, code, bc):
    return str(pc) + " " + bytecode.bytecodes[ord(code[pc])]

driver = jit.JitDriver(greens = ['pc', 'code', 'bc'],
                       reds = ['frame'],
                       virtualizables=['frame'],
                       get_printable_location=printable_loc)

class W_Root(object):
    pass

class W_IntObject(W_Root):
    def __init__(self, intval):
        self.intval = intval

    def add(self, other):
        if not isinstance(other, W_IntObject):
            raise Exception("wrong type")
        return W_IntObject(self.intval + other.intval)

    def lt(self, other): 
        if not isinstance(other, W_IntObject):
            raise Exception("wrong type")
        return W_IntObject(self.intval < other.intval)

    def is_true(self):
        return self.intval != 0

    def str(self):
        return str(self.intval)

class W_FloatObject(W_Root):
    def __init__(self, floatval):
        self.floatval

    #def add(self, other):
    #    xxxx

class Frame(object):
    _virtualizable_ = ['valuestack[*]', 'valuestack_pos', 'vars[*]']
    
    def __init__(self, bc):
        self = jit.hint(self, fresh_virtualizable=True, access_directly=True)
        self.valuestack = [None] * 3 # safe estimate!
        self.vars = [None] * bc.numvars
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
            frame.push(W_IntObject(bc.constants[arg]))
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
            driver.can_enter_jit(pc=pc, code=code, bc=bc, frame=frame)
        elif c == bytecode.PRINT:
            item = frame.pop()
            print item.str()
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
