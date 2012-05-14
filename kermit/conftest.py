def pytest_addoption(parser):
    group = parser.getgroup("pypy options")
    group.addoption('--view', action="store_true",
           default=False, dest="view",
           help="show only the compiled loops")
    group.addoption('--viewloops', action="store_true",
           default=False, dest="viewloops",
           help="show only the compiled loops")

def pytest_configure(config):
    from pypy import conftest
    conftest.option = config.option
    
