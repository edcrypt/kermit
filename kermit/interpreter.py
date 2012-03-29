
from kermit.sourceparser import parse
from kermit.bytecode import compile_ast
from kermit import bytecode

class Frame(object):
    def __init__(self, bc):
        self.valuestack = [0] * 100 # safe estimate!
        self.vars = [0] * bc.numvars
        self.valuestack_pos = 0

    def push(self, v):
        self.valuestack[self.valuestack_pos] = v
        self.valuestack_pos += 1
    
    def pop(self):
        v = self.valuestack[self.valuestack_pos - 1]
        self.valuestack_pos -= 1
        return v

def add(left, right):
    return left + right

def execute(frame, bc):
    code = bc.code
    pc = 0
    while True:
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
        elif c == bytecode.PRINT:
            item = frame.pop()
            print item
        else:
            assert False

def interpret(source):
    bc = compile_ast(parse(source))
    frame = Frame(bc)
    execute(frame, bc)
    return frame # for tests and later introspection
