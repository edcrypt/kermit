
bytecodes = [
    'LOAD_CONSTANT', 'LOAD_STRING', 'LOAD_VAR',
    'ASSIGN', 'DISCARD_TOP', 'JUMP_IF_FALSE', 'JUMP_BACKWARD',
    'BINARY_ADD', 'BINARY_SUB', 'BINARY_EQ', 'RETURN', 'PRINT',
    'BINARY_LT'
]


for i, bytecode in enumerate(bytecodes):
    globals()[bytecode] = i


BINOP = {
    '+': globals()["BINARY_ADD"],
    '-': globals()["BINARY_SUB"],
    '==': globals()["BINARY_EQ"],
    '<': globals()["BINARY_LT"]
}


class ByteCode(object):
    _immutable_fields_ = ['code', 'constants[*]', 'strconstants[*]', 'numvars']

    def __init__(self, code, constants, strconstants, numvars):
        self.code = code
        self.constants = constants
        self.strconstants = strconstants
        self.numvars = numvars

    def dump(self):
        lines = []
        i = 0
        for i in range(0, len(self.code), 2):
            c = self.code[i]
            c2 = self.code[i + 1]
            lines.append(bytecodes[ord(c)] + " " + str(ord(c2)))
        return '\n'.join(lines)
