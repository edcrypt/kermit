
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

    def test_float(self):
        self.check_compile("1.0;", '''
        LOAD_CONSTANT 0
        DISCARD_TOP 0
        RETURN 0
        ''')

    def test_add_floats(self):
        self.check_compile('1.5 + .5;', '''
        LOAD_CONSTANT 0
        LOAD_CONSTANT 1
        BINARY_ADD 0
        DISCARD_TOP 0
        RETURN 0
        ''')

    def test_lt_floats(self):
        self.check_compile('1.5 < .5;', '''
        LOAD_CONSTANT 0
        LOAD_CONSTANT 1
        BINARY_LT 0
        DISCARD_TOP 0
        RETURN 0
        ''')

    def test_print(self):
        self.check_compile('print a;', '''
        LOAD_VAR 0
        PRINT 0
        RETURN 0
        ''')

    def test_while(self):
        self.check_compile('while (1) { print 1; }', '''
        LOAD_CONSTANT 0
        JUMP_IF_FALSE 10
        LOAD_CONSTANT 1
        PRINT 0
        JUMP_BACKWARD 0
        RETURN 0
        ''')

    def test_if(self):
        self.check_compile('''
        if (a) {
           1;
        }
        ''', '''
        LOAD_VAR 0
        JUMP_IF_FALSE 8
        LOAD_CONSTANT 0
        DISCARD_TOP 0
        RETURN 0
        ''')
