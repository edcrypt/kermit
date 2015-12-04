def string_unquote(s):
    assert len(s) >= 2
    assert s[0] == "\""
    assert s[-1] == "\""

    s = s[:-1]
    s = s[1:]

    return s
