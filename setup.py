#!/usr/bin/env python

from glob import glob
from imp import new_module
from os import getcwd, path


from setuptools import setup, find_packages


version = new_module("version")

exec(
    compile(
        open(
            path.join(
                path.dirname(
                    globals().get(
                        "__file__",
                        path.join(getcwd(), "kermit")
                    )
                ),
                "kermit/version.py"
            ),
            "r"
        ).read(),
        "kermit/version.py",
        "exec"
    ),
    version.__dict__
)


setup(
    name="keermit",
    version=version.version,
    description="TBA",
    long_description="{0:s}\n\n{1:s}".format(
        open("README.rst").read(), open("CHANGES.rst").read()
    ),
    author="TBA",
    author_email="TBA",
    url="TBA",
    download_url="TBA",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Interpreters",
    ],
    license="TBA",
    keywords="TBA",
    platforms="POSIX",
    packages=find_packages("."),
    # package_data={
    #     "kermit": [
    #         "lib/*.kermit",
    #     ]
    # },
    # include_package_data=True,
    scripts=glob("bin/*"),
    install_requires=[
    ],
    setup_requires=[
        "fabric",
        "pytest",
        "pypy",
        "rpython",
    ],
    entry_points={
        "console_scripts": [
            "kermit=kermit.main:entrypoint",
        ]
    },
    test_suite="tests.main.main",
    zip_safe=False
)
