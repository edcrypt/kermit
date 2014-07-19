# Target:   kermit
# Date:     19th July 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""RPython Entry Point: kermit"""


from rpython.jit.codewriter.policy import JitPolicy


from kermit.main import main


def target(*args):
    return main, None


def jitpolicy(driver):
    return JitPolicy()
