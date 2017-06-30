#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

from __future__ import unicode_literals

import os

import click

from git_ext.utils import logging
from git_ext.git import get_repo_slug
from git_ext.bitbucket.pullrequests import PullRequests

logger = logging.getLogger(__name__)
current_path = os.getcwd()

@click.group()
def pullrequests():
    pass

@pullrequests.command()
def list():
    username, repo_slug = get_repo_slug()
    prs = PullRequests(username, repo_slug)
    for pr in prs.pullrequests_list():
        click.echo("#{} {}".format(*pr))


if __name__ == '__main__':
    pullrequests()
