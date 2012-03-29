
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
        star = node.children[0]
        stmts = []
        while len(star.children) == 2:
            stmts.append(self.visit_stmt(star.children[0]))
            star = star.children[1]
        stmts.append(self.visit_stmt(star.children[0]))
        return Block(stmts)

    def visit_stmt(self, node):
        if len(node.children) == 2:
            return Stmt(self.visit_expr(node.children[0]))
        if len(node.children) == 4:
            return Assignment(node.children[0].additional_info,
                              self.visit_expr(node.children[2]))
        raise NotImplementedError

    def visit_expr(self, node):
        if len(node.children) == 1:
            return self.visit_atom(node.children[0])
        return BinOp(node.children[1].additional_info,
                     self.visit_atom(node.children[0]),
                     self.visit_expr(node.children[2]))

    def visit_atom(self, node):
        chnode = node.children[0]
        if chnode.symbol == 'DECIMAL':
            return ConstantInt(int(chnode.additional_info))
        if chnode.symbol == 'VARIABLE':
            return Variable(chnode.additional_info)
        raise NotImplementedError

transformer = Transformer()

def parse(source):
    """ Parse the source code and produce an AST
    """
    return transformer.visit_main(_parse(source))
