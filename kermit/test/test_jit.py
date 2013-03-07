
from rpython.jit.metainterp.test.support import LLJitMixin
from kermit.interpreter import interpret

class TestJit(LLJitMixin):
    def test_jit(self):
        codes = ['print 1', 'n = 0; while (n < 10) { n = n + 1; }']
        def main(i):
            interpret(codes[i])
        self.meta_interp(main, [1], listops=True)
