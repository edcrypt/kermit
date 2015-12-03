"""AST"""


from kermit import bytecode


class Node(object):

    """ The abstract AST node
    """

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other


class Block(Node):

    """ A list of statements
    """

    def __init__(self, stmts):
        self.stmts = stmts

    def compile(self, ctx):
        for stmt in self.stmts:
            stmt.compile(ctx)


class Stmt(Node):

    """ A single statement
    """

    def __init__(self, expr):
        self.expr = expr

    def compile(self, ctx):
        self.expr.compile(ctx)
        ctx.emit(bytecode.DISCARD_TOP)


class ConstantInt(Node):

    """ Represent a constant
    """

    def __init__(self, intval):
        self.intval = intval

    def compile(self, ctx):
        # convert the integer to W_IntObject already here
        from kermit.objects import W_IntObject
        w = W_IntObject(self.intval)
        ctx.emit(bytecode.LOAD_CONSTANT, ctx.register_constant(w))


class ConstantFloat(Node):

    """ Represent a constant
    """

    def __init__(self, floatval):
        self.floatval = floatval

    def compile(self, ctx):
        # convert the integer to W_FloatObject already here
        from kermit.objects import W_FloatObject
        w = W_FloatObject(self.floatval)
        ctx.emit(bytecode.LOAD_CONSTANT, ctx.register_constant(w))


class ConstantString(Node):
    """Represent a constant String"""

    def __init__(self, stringval):
        self.stringval = stringval

    def compile(self, ctx):
        # convert the integer to W_StringObject already here
        from kermit.objects import W_StringObject
        w = W_StringObject(self.stringval)
        ctx.emit(
            bytecode.LOAD_STRING, ctx.register_string(w)
        )


class BinOp(Node):

    """ A binary operation
    """

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def compile(self, ctx):
        self.left.compile(ctx)
        self.right.compile(ctx)
        ctx.emit(bytecode.BINOP[self.op])


class Variable(Node):

    """ Variable reference
    """

    def __init__(self, varname):
        self.varname = varname

    def compile(self, ctx):
        ctx.emit(bytecode.LOAD_VAR, ctx.register_var(self.varname))


class Assignment(Node):

    """ Assign to a variable
    """

    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr

    def compile(self, ctx):
        self.expr.compile(ctx)
        ctx.emit(bytecode.ASSIGN, ctx.register_var(self.varname))


class While(Node):

    """ Simple loop
    """

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def compile(self, ctx):
        pos = len(ctx.data)
        self.cond.compile(ctx)
        ctx.emit(bytecode.JUMP_IF_FALSE, 0)
        jmp_pos = len(ctx.data) - 1
        self.body.compile(ctx)
        ctx.emit(bytecode.JUMP_BACKWARD, pos)
        ctx.data[jmp_pos] = chr(len(ctx.data))


class If(Node):

    """ A very simple if
    """

    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def compile(self, ctx):
        self.cond.compile(ctx)
        ctx.emit(bytecode.JUMP_IF_FALSE, 0)
        jmp_pos = len(ctx.data) - 1
        self.body.compile(ctx)
        ctx.data[jmp_pos] = chr(len(ctx.data))


class Print(Node):

    def __init__(self, expr):
        self.expr = expr

    def compile(self, ctx):
        self.expr.compile(ctx)
        ctx.emit(bytecode.PRINT, 0)
