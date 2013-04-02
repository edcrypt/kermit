
from kermit.interpreter import interpret

def test_interp():
    interpret('1 + 2;')
    # nothing to assert

def test_print(capfd):
    interpret('print 1;')
    out, err = capfd.readouterr()
    assert out == '1\n'

def test_float_add(capfd):
    interpret('print 1.5 + .5;')
    out, err = capfd.readouterr()
    assert out == '2.0\n' and not err

def test_float_lt(capfd):
    interpret('print 1.5 < .5;')
    out, err = capfd.readouterr()
    assert out == 'False\n' and not err
    
def test_while():
    interpret('n = 0; while (n < 10) { n = n + 1; }')

def test_if(capfd):
    interpret('''
    if (1) {
       print 2;
    }
    ''')
    out, err = capfd.readouterr()
    assert out == '2\n'
