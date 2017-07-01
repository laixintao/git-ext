#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, no-value-for-parameter, unexpected-keyword-arg
import os
import re
import commands
import json

import click
import arrow

from git_ext.utils import logging
from git_ext.git import get_repo_slug, get_git_core_editor, get_dotgit_abs_path
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
    pr_list = prs.pullrequests_list()
    logger.info(pr_list)
    for pr in pr_list:
        click.echo(u"#{} {} by {}({updated_on})".format(updated_on=arrow.get(pr[3]).humanize(), *pr))
    if not pr_list:
        click.echo("No open PRs in this repo.")

@pullrequests.command()
@click.pass_context
@click.option('--id', '-i', help="pullrequests' id")
def activity(ctx, id):
    prs = ctx.obj['prs']
    for activity in prs.pullrequests_activity(id):
        echo_time = click.style(arrow.get(activity[1]).humanize(), fg='green')
        echo_action = click.style("{} {} this PR:".format(activity[2], activity[0]), fg='yellow')
        click.echo(echo_time+ ' ' + echo_action)
        click.echo(activity[3])

@pullrequests.command()
@click.pass_context
@click.argument('source_branch')
@click.argument('destination_branch')
def create(ctx, source_branch, destination_branch):
    # TODO abort if no commit message
    logger.info("base branch: {}, head branch: {}".format(source_branch, destination_branch))
    temp_submit_file = os.path.join(get_dotgit_abs_path(), '.git_ext.temp')
    os.system(get_git_core_editor() + " " + temp_submit_file)
    with open(temp_submit_file, 'r') as commit_file:
        lines = commit_file.readlines()
        title = lines[0]
        desc = "".join(lines[1:])
    os.remove(temp_submit_file)
    reviewers_raw = raw_input("Reviewers(start with @):")
    reviewers = "".join(reviewers_raw.split()).split('@')[1:]  # thy there is a space??
    prs = ctx.obj['prs']
    resp = prs.create(source_branch, destination_branch, reviewers, title, desc)
    if resp.status_code == 201:
        click.echo(json.dumps(resp.json(), indent=2, sort_keys=True))
    else:
        click.echo(click.style("ERROR!", fg='red'))
        click.echo(json.dumps(resp.json(), indent=2, sort_keys=True))


if __name__ == '__main__':
    pullrequests(obj={})
