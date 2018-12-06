# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from requests.auth import HTTPBasicAuth
import arrow
import click
from abc import ABCMeta, abstractmethod
from git_ext.utils import logging
from git_ext.git import get_repo_slug

PR_DISPLAY_FORMAT = "#{_id} {title} [{source_branch}->{dest_branch}]  by {author}"

logger = logging.getLogger(__name__)


class User(object):
    def __init__(self, username, password=None):
        self.username = username
        if password:
            self.password = password
            self.auth = HTTPBasicAuth(self.username, self.password)


class Activity(object):
    "Pull request's activity, like comment, approval etc"

    COMMENT_TYPE = "comment"
    APPROVAL_TYPE = "approve"
    UPDATE_TYPE = "update"

    def __init__(self, username, content, type, time):
        self.type = type
        self.username = username
        self.content = content
        self.time = time

    def __str__(self):
        pass

    def to_echo(self):
        echo_user = click.style(self.username, fg="green")
        echo_action_time = click.style(
            " {} this PR {}:".format(
                self.type, arrow.get(self.time).humanize(), fg="yellow"
            )
        )
        display = echo_user + " " + echo_action_time + "\n" + self.content
        return display


class PullRequest(object):
    def __init__(
        self,
        _id,
        source_branch,
        dest_branch,
        author,
        reviewers,
        title,
        description,
        pr_view_url="",
    ):
        """
        :param reviewers: list consist of str
        others: string
        """
        self._id = _id
        self.source_branch = source_branch
        self.dest_branch = dest_branch
        self.author = author
        self.reviewers = reviewers
        self.title = title
        self.description = description
        self.pr_view_url = pr_view_url

    def __str__(self):
        return PR_DISPLAY_FORMAT.format(**self.__dict__)


class Remote(object):
    "Define a remote's behavior, like submit a pr, or check activities."

    __metaclass__ = ABCMeta

    def __init__(self, user=None):
        """
        :param user: User
        :param repo_username, repo_name: for url formatting, like laixintao/git-ext.
        """

        self.repo_username, self.repo_name = get_repo_slug()
        if user:
            self.user = user
        else:
            self.user = User(self.repo_username)

    @abstractmethod
    def get_all_pullrequests(self):
        """Get all open pullrequests.
        TODO Turn page
        TODO -a=all prs
        :return pullrequest_list: PullReuqest lists"""
        pass

    @abstractmethod
    def submit_new_pr(self, pr):
        pass

    @abstractmethod
    def get_activities(self, pr_id):
        "get activities for a spcific pull request"
        # TODO turn page use next
        # TODO staticmethod
        # TODO more pretty return values
        pass
