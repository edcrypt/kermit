
import py
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from kermit import kermitdir

grammar = py.path.local(kermitdir).join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)

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
