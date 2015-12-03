"""Compiler"""


from kermit.bytecode import ByteCode, RETURN


class CompilerContext(object):

    def __init__(self):
        self.data = []
        self.constants = []
        self.strconstants = []
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

    def emit(self, bc, arg=0):
        self.data.append(chr(bc))
        self.data.append(chr(arg))

    def create_bytecode(self):
        return ByteCode(
            "".join(self.data),
            self.constants[:],
            self.strconstants[:],
            len(self.names)
        )


def compile(astnode):
    c = CompilerContext()
    astnode.compile(c)
    c.emit(RETURN, 0)  # noqa
    return c.create_bytecode()
