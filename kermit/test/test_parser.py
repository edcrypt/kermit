
from kermit.sourceparser import parse, Stmt, Block, ConstantInt, BinOp,\
     Variable

def test_parse_basic():
    assert parse('13;') == Block([Stmt(ConstantInt(13))])
    assert parse('1 + 2;') == Block([Stmt(BinOp("+", ConstantInt(1),
                                                ConstantInt(2)))])
    assert parse('1 + a;') == Block([Stmt(BinOp('+', ConstantInt(1),
                                                Variable('a')))])
    
