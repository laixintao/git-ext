#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, no-value-for-parameter, unexpected-keyword-arg
from __future__ import absolute_import

import os
import re
import commands
import json

import click
import arrow

from git_ext.utils import logging, get_reviewers_group, check_reviewers_group
from git_ext.git import get_repo_slug, get_git_core_editor, get_dotgit_abs_path
from git_ext.git import init_commit_editmsg_file, read_commit_editmsg_file
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
        click.echo(pr)
    if not pr_list:
        click.echo("No open PRs in this repo.")

@pullrequests.command(help="Show a pr's activity, display lastest 10 messages by default")
@click.pass_context
@click.argument('id')
def activity(ctx, id):
    # TODO move colors to color-theme config file
    prs = ctx.obj['prs']
    for activity in prs.pullrequests_activity(id):
        echo_user = click.style(activity[2], fg='green')
        echo_action_time = click.style(" {} this PR {}:".format(activity[0],
                                                                arrow.get(activity[1]).humanize()), fg='yellow')
        click.echo(echo_user+ ' ' + echo_action_time)
        click.echo(activity[3])

@pullrequests.command()
@click.pass_context
@click.argument('source_branch')
@click.argument('destination_branch')
def create(ctx, source_branch, destination_branch):
    logger.info("base branch: {}, head branch: {}".format(source_branch, destination_branch))
    pr_submit_file = init_commit_editmsg_file()
    os.system(get_git_core_editor() + " " + pr_submit_file)
    title, desc = read_commit_editmsg_file(pr_submit_file)
    if not title:
        click.echo("Creating pullrequests aborted!")
        click.echo("Title is blank.")
        # TODO exit value
        return
    click.echo("Custom groups:")
    reviewers_group = get_reviewers_group()
    for group in reviewers_group:
        click.echo("@{} = {}".format(group, reviewers_group[group]))
    reviewers_raw = raw_input("Reviewers(start with @):")
    final_reviewers = check_reviewers_group(reviewers_raw)
    prs = ctx.obj['prs']
    resp = prs.create(source_branch, destination_branch, final_reviewers, title, desc)
    if resp.status_code == 201:
        click.echo(click.style("201 Created!", fg='green'))
        click.echo(PullRequests.output(resp.json()))
        reviewers = [user['username'] for user in resp.json()['reviewers']]
        click.echo(click.style("Reviewers: ", fg='yellow') + " ".join(reviewers))
    else:
        click.echo(click.style("ERROR!", fg='red'))
        click.echo(json.dumps(resp.json(), indent=2, sort_keys=True))

def main():
    pullrequests(obj={})

if __name__ == '__main__':
    main()
