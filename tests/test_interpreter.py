from pytest import fixture, raises


from kermit.interpreter import interpret, printable_loc, Interpreter


@fixture
def interpreter(request):
    return Interpreter()


def test_printable_loc():
    from kermit import bytecode

    i = 0
    pc = 0
    bc = [chr(i)]

    assert (
        printable_loc(pc, bc) == "{0} {1}".format(pc, bytecode.bytecodes[i])
    )


def test_interp():
    interpret('1 + 2;')
    # nothing to assert


def test_interpreter_runstring(interpreter):
    interpreter.runstring('1 + 2;')
    # nothing to assert


def test_interpreter_runfile(interpreter, tmpdir):
    f = tmpdir.ensure("foo.ker")
    f.write("1 + 1;")
    interpreter.runfile(str(f))
    # nothing to assert


def test_print(capfd):
    interpret('print 1;')
    out, err = capfd.readouterr()
    assert out == '1\n'


def test_int_add(capfd):
    interpret('print 1 + 5;')
    out, err = capfd.readouterr()
    assert out == '6\n' and not err


def test_add_int_error():
    with raises(Exception):
        interpret('1 + .5;')


def test_int_lt(capfd):
    interpret('print 1 < 5;')
    out, err = capfd.readouterr()
    assert out == 'True\n' and not err


def test_int_lt_int_error(capfd):
    with raises(Exception):
        interpret('1 < .5;')


def test_float_add(capfd):
    interpret('print 1.5 + .5;')
    out, err = capfd.readouterr()
    assert out == '2.0\n' and not err


def test_float_add_int_error():
    with raises(Exception):
        interpret('1.5 + 5;')


def test_float_lt(capfd):
    interpret('print 1.5 < .5;')
    out, err = capfd.readouterr()
    assert out == 'False\n' and not err


def test_float_lt_int_error(capfd):
    with raises(Exception):
        interpret('1.5 < 5;')


def test_string_add(capfd):
    interpret('print "foo" + "bar";')
    out, err = capfd.readouterr()
    assert out == 'foobar\n' and not err


def test_string_add_other_error():
    with raises(Exception):
        interpret('"foo" + 5;')


def test_string_lt(capfd):
    interpret('print "foo" < "bar";')
    out, err = capfd.readouterr()
    assert out == 'False\n' and not err


def test_string_lt_other_error(capfd):
    with raises(Exception):
        interpret('"foo" < 5;')


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


def test_func(capfd):
    interpret('''
    func hello() {
      print "Hello World!";
    }

    hello();
    ''')

    out, err = capfd.readouterr()
    assert out == 'Hello World!\n'
