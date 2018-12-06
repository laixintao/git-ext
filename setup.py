# -*- coding: utf-8 -*-

import os
from codecs import open
from setuptools import setup, find_packages

VERSION = "0.6.0"
DESCRIPTION = "A git extension that allows you submit pullrequests from command line."

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), "r") as f:
    readme = f.read()

with open(os.path.join(here, "requirements.txt"), "r") as f:
    requires = f.read()

setup(
    name="git-ext",
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme,
    author="laixintao",
    author_email="laixintao1995@163.com",
    url="https://github.com/laixintao/git-ext",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    license="GNU",
    zip_safe=False,
    # TODO use install to generic yml file cmdclass={'git-pullrequests': PyTest},
    entry_points={
        "console_scripts": [
            "git-pullrequest = git_ext.bin.pullrequest:main",
            "init-git-ext = git_ext.bin.init_git_ext:main",
        ],
        "gui_scripts": [],
    },
)
