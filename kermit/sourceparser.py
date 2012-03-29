
import py
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from kermit import kermitdir

grammar = py.path.local(kermitdir).join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)

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

class Stmt(Node):
    """ A single statement
    """
    def __init__(self, expr):
        self.expr = expr

class ConstantInt(Node):
    """ Represent a constant
    """
    def __init__(self, intval):
        self.intval = intval

class BinOp(Node):
    """ A binary operation
    """
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Variable(Node):
    """ Variable reference
    """
    def __init__(self, varname):
        self.varname = varname

class Assignment(Node):
    """ Assign to a variable
    """
    def __init__(self, varname, expr):
        self.varname = varname
        self.expr = expr

class Transformer(object):
    """ Transforms AST from the obscure format given to us by the ennfparser
    to something easier to work with
    """
    def visit_main(self, node):
        xxx

transformer = Transformer()

def parse(source):
    """ Parse the source code and produce an AST
    """
    return transformer.visit_main(_parse(source))
