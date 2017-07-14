=======
git-ext
=======

.. image :: https://img.shields.io/badge/pypi-v0.1-green.svg
    :target: https://pypi.python.org/pypi/git-ext
.. image :: https://img.shields.io/codecov/c/github/laixintao/git-ext.svg
    :target: https://codecov.io/gh/laixintao/git-ext
.. image :: https://travis-ci.org/laixintao/git-ext.svg?branch=master
    :target: https://travis-ci.org/laixintao/git-ext


A git extension that allows you submit pullrequests from command line.

Current support bitbucket only, add github and gitlab in the future.

install
-------

Use pip to install.::

    pip install git-ext

Then run init-git-ext command to write your bitbucket account infomation to ~/.git_ext.yml(Pullrequests need account info with HTTP BASIC AUTH.::

    init-git-ext

Optional
--------

You can add a git alias if you are lazy like me :)::

    git config --global alias.pr pullrequest  


usage
-----
::

    $ git pullrequest create test_b master
    Reviewers(start with @):
    201 Created!
    #2 This is your commit title.[test_b->master]  by boson_laixintao(just now)
    Reviewers:

    $ git pullrequest list
    #2 This is your commit title.[test_b->master]  by boson_laixintao(just now)

    $ git pullrequest
    Usage: git-pullrequests [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      activity  Show a pr's activity, display lastest 10...
      create
      list

Develop
-------

Export a enviroment to see the logs::
    
    export GITEXT=debug


Licenses
--------

GPLv3
