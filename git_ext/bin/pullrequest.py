#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, no-value-for-parameter, unexpected-keyword-arg
from __future__ import absolute_import, unicode_literals

import os
import json

import click

from git_ext.utils import logging, get_reviewers_group, check_reviewers_group
from git_ext.git import get_git_core_editor, backup_commit_file
from git_ext.git import init_commit_editmsg_file, read_commit_editmsg_file, get_commit_editmsg_bak_abs_path
from git_ext import PullRequest
from git_ext.bitbucket import BitbucketRemote

logger = logging.getLogger(__name__)
current_path = os.getcwd()


def get_remote():
    # TODO determine which remote to use
    return BitbucketRemote()


@click.group()
@click.pass_context
def pullrequests(ctx):
    ctx.obj['remote'] = get_remote()


@pullrequests.command()
@click.pass_context
def list(ctx):
    remote = ctx.obj['remote']
    pr_list = remote.get_all_pullrequests()
    for pr in pr_list:
        click.echo(pr)
    if not pr_list:
        click.echo("No open PRs in this repo.")


@pullrequests.command(help="Show a pr's activity, display lastest 10 messages by default")
@click.pass_context
@click.argument('id')
def activity(ctx, id):
    # TODO move colors to color-theme config file
    remote = ctx.obj['remote']
    for activity in remote.get_activities(id):
        click.echo(activity.to_echo())


@pullrequests.command()
@click.pass_context
@click.argument('source_branch')
@click.argument('destination_branch')
def create(ctx, source_branch, destination_branch):
    logger.info("base branch: {}, head branch: {}".format(source_branch, destination_branch))
    pr_submit_file = init_commit_editmsg_file(source_branch, destination_branch)
    os.system(get_git_core_editor() + " " + pr_submit_file)
    title, desc = read_commit_editmsg_file(pr_submit_file)
    if not title:
        click.echo("Title is blank.")
        raise click.Abort
    # backup commit file
    backup_commit_file()
    reviewers_group = get_reviewers_group()
    if reviewers_group:
        click.echo("Custom groups:")
        for group, member in reviewers_group.items():
            click.echo("{}={}".format(group, member))
    else:
        click.echo("No reviewers group found, you can custom reviewers group in ~/.git_ext.yml")
    reviewers_raw = raw_input("Reviewers(start with @):")
    final_reviewers = check_reviewers_group(reviewers_raw)
    remote = ctx.obj['remote']
    pr = PullRequest('', source_branch, destination_branch, remote.user.username, final_reviewers, title, desc)
    resp = remote.submit_new_pr(pr)
    if resp.status_code == 201:
        # delete backup commit file
        os.remove(get_commit_editmsg_bak_abs_path())
        click.echo(click.style("201 Created!", fg='green'))
        click.echo(pr)
        reviewers = [user['username'] for user in resp.json()['reviewers']]
        click.echo(click.style("Reviewers: ", fg='yellow') + " ".join(reviewers))
    else:
        click.echo(click.style("ERROR!", fg='red'))
        click.echo(json.dumps(resp.json(), indent=2, sort_keys=True))


def main():
    pullrequests(obj={})


if __name__ == '__main__':
    main()
