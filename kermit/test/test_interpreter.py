
from kermit.interpreter import interpret

def test_interp():
    interpret('1 + 2;')
    # nothing to assert

def test_print(capfd):
    interpret('print 1;')
    out, err = capfd.readouterr()
    assert out == '1\n'
