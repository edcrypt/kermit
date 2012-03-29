
from kermit.sourceparser import parse, Stmt, Block, ConstantInt, BinOp,\
     Variable, Assignment, While, If

def test_parse_basic():
    assert parse('13;') == Block([Stmt(ConstantInt(13))])
    assert parse('1 + 2;') == Block([Stmt(BinOp("+", ConstantInt(1),
                                                ConstantInt(2)))])
    assert parse('1 + a;') == Block([Stmt(BinOp('+', ConstantInt(1),
                                                Variable('a')))])

def test_multiple_statements():
    assert parse('''
    1 + 2;
    c;
    e;
    ''') == Block([Stmt(BinOp("+", ConstantInt(1), ConstantInt(2))),
                   Stmt(Variable('c')),
                   Stmt(Variable('e'))])

def test_assignment():
    assert parse('a = 3;') == Block([Assignment('a', ConstantInt(3))])

def test_while():
    assert parse('while (1) { a = 3; }') == Block([While(ConstantInt(1),
              Block([Assignment('a', ConstantInt(3))]))])

def test_if():
    assert parse("if (1) { a; }") == Block([If(ConstantInt(1),
                                               Block([Stmt(Variable("a"))]))])
