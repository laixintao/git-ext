# git-ext

[![Codecov](https://img.shields.io/codecov/c/github/laixintao/git-ext.svg)](https://codecov.io/gh/laixintao/git-ext)
![](https://travis-ci.org/laixintao/git-ext.svg?branch=master)

A git extension that allows you submit pullrequests from command line.

## usage

    $ git pullrequests create test_b master
    Reviewers(start with @):
    201 Created!
    #2 This is your commit title.[test_b->master]  by boson_laixintao(just now)
    Reviewers:

    $ git pullrequests list
    #2 This is your commit title.[test_b->master]  by boson_laixintao(just now)

    $ git pullrequests
    Usage: git-pullrequests [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      activity  Show a pr's activity, display lastest 10...
      create
      list
     ~/Documents/program/program/test-gitext   test_b  git pullrequests --help
