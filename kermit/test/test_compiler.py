
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
        RETURN 0
        ''')

    def test_add(self):
        self.check_compile('a + 1;', '''
        LOAD_VAR 0
        LOAD_CONSTANT 0
        BINARY_ADD 0
        DISCARD_TOP 0
        RETURN 0
        ''')

    def test_print(self):
        self.check_compile('print a;', '''
        LOAD_VAR 0
        PRINT 0
        RETURN 0
        ''')
