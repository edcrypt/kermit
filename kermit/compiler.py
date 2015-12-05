"""Compiler"""


from kermit.bytecode import ByteCode, RETURN


class CompilerContext(object):

    def __init__(self):
        self.data = []
        self.constants = []
        self.strconstants = []
        self.functions = []
        self.names = []
        self.names_to_numbers = {}

    def register_constant(self, v):
        self.constants.append(v)
        return len(self.constants) - 1

    def register_string(self, v):
        self.strconstants.append(v)
        return len(self.strconstants) - 1

    def register_var(self, name):
        try:
            return self.names_to_numbers[name]
        except KeyError:
            self.names_to_numbers[name] = len(self.names)
            self.names.append(name)
            return len(self.names) - 1

    def register_func(self, f):
        self.functions.append(f)
        return len(self.functions) - 1

    def emit(self, bc, arg=0):
        self.data.append(chr(bc))
        self.data.append(chr(arg))

    def create_bytecode(self):
        return ByteCode(
            "".join(self.data),
            self.constants[:],
            self.strconstants[:],
            self.functions[:],
            len(self.names)
        )


class Compiler(object):

    def __init__(self):
        self.ctx = CompilerContext()

    def compile(self, ast):
        self.ctx.data = []
        ast.compile(self.ctx)
        self.ctx.emit(RETURN, 0)
        return self.ctx.create_bytecode()


def compile_ast(ast):
    return Compiler().compile(ast)
