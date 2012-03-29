
from kermit.sourceparser import parse
from kermit.bytecode import compile_ast

class TestCompiler(object):
    def check_compile(self, source, expected):
        bc = compile_ast(parse(source))
        assert [i.strip() for i in expected.splitlines() if i.strip()] == bc.dump().splitlines()

    def test_basic(self):
        self.check_compile("1;", '''
        LOAD_CONSTANT 0
        DISCARD_TOP 0
        ''')
