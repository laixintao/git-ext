#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, no-value-for-parameter, unexpected-keyword-arg
import os

import click
import arrow

from git_ext.utils import logging
from git_ext.git import get_repo_slug
from git_ext.bitbucket.pullrequests import PullRequests

logger = logging.getLogger(__name__)
current_path = os.getcwd()


@click.group()
@click.pass_context
def pullrequests(ctx):
    username, repo_slug = get_repo_slug()
    ctx.obj['prs'] = PullRequests(username, repo_slug)


@pullrequests.command()
@click.pass_context
def list(ctx):
    prs = ctx.obj['prs']
    for pr in prs.pullrequests_list():
        click.echo(u"#{} {}".format(*pr))

@pullrequests.command()
@click.pass_context
@click.option('--id', '-i', help="pullrequests' id")
def activity(ctx, id):
    prs = ctx.obj['prs']
    for activity in prs.pullrequests_activity(id):
        click.echo(arrow.get(activity[1]).humanize()+'->')
        click.echo("\t{} {}: {}".format(activity[2], activity[0], activity[3]))


if __name__ == '__main__':
    pullrequests(obj={})
