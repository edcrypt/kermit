
from kermit.interpreter import interpret

def test_interp():
    interpret('1 + 2;')
    # nothing to assert

def test_print(capfd):
    interpret('print 1;')
    out, err = capfd.readouterr()
    assert out == '1\n'

def test_while():
    interpret('n = 0; while (n < 10) { n = n + 1; }')
