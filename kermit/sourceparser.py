
import py
from pypy.rlib.parsing.ebnfparse import parse_ebnf, make_parse_function
from kermit import kermitdir

grammar = py.path.local(kermitdir).join('grammar.txt').read("rt")
regexs, rules, ToAST = parse_ebnf(grammar)
_parse = make_parse_function(regexs, rules, eof=True)

class Transformer(object):
    def visit_main(self, node):
        xxx

transformer = Transformer()

def parse(source):
    return transformer.visit_main(_parse(source))
