"""Parser"""


import py

from rpython.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function


from kermit import kermitdir

from kermit.ast import (
    Stmt, Block, ConstantInt, ConstantFloat, Function, Call,
    ConstantString, BinOp, Variable, Assignment, While, If, Print
)

from kermit.utils import string_unquote


grammar = py.path.local(kermitdir).join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)


class Transformer(object):

    """ Transforms AST from the obscure format given to us by the ennfparser
    to something easier to work with
    """

    def _grab_stmts(self, star):
        stmts = []
        while len(star.children) == 2:
            stmts.append(self.visit_stmt(star.children[0]))
            star = star.children[1]
        stmts.append(self.visit_stmt(star.children[0]))
        return stmts

    def visit_main(self, node):
        stmts = self._grab_stmts(node.children[0])
        return Block(stmts)

    def visit_stmt(self, node):
        if len(node.children) == 2:
            return Stmt(self.visit_expr(node.children[0]))
        if len(node.children) == 4:
            return Assignment(node.children[0].additional_info,
                              self.visit_expr(node.children[2]))
        if node.children[0].additional_info == 'while':
            cond = self.visit_expr(node.children[2])
            stmts = self._grab_stmts(node.children[5])
            return While(cond, Block(stmts))
        if node.children[0].additional_info == 'if':
            cond = self.visit_expr(node.children[2])
            stmts = self._grab_stmts(node.children[5])
            return If(cond, Block(stmts))
        if node.children[0].additional_info == 'func':
            name = node.children[1].additional_info
            body = self._grab_stmts(node.children[5])
            return Function(name, Block(body))
        if node.children[0].additional_info == 'print':
            return Print(self.visit_expr(node.children[1]))
        raise NotImplementedError

    def visit_expr(self, node):
        chnode = node.children[0]
        if chnode.symbol == "call":
            return Call(Variable(chnode.children[0].additional_info))
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
        if chnode.symbol == 'FLOAT':
            return ConstantFloat(float(chnode.additional_info))
        if chnode.symbol == 'STRING':
            return ConstantString(
                str(string_unquote(chnode.additional_info))
            )
        raise NotImplementedError


transformer = Transformer()


def parse(source):
    """ Parse the source code and produce an AST
    """
    return transformer.visit_main(_parse(source))
