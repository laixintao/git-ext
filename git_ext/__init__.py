# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import json
import requests
import arrow
from abc import ABCMeta, abstractmethod
from git_ext.bitbucket.user import user_auth
from git_ext.bitbucket import urls
from git_ext.utils import logging

PR_ECHO_STRING = "#{id} {title}[{source}->{dest}]  by {author}({last_update})"

logger = logging.getLogger(__name__)


class Activity(object):
    "Pull request's activity, like comment, approval etc"

    COMMENT_TYPE = 'comment'
    APPROVAL_TYPE = 'approval'
    UPDATE_TYPE = 'update'

    def __init__(self, username, content, type, time):
        self.type = type
        self.username = username
        self.content = content
        self.time = time

    def __str__(self):
        pass


class PullRequest(object):
    __metaclass__ = ABCMeta

    def __init__(self, user, repo_username, repo_name, *args, **kwargs):
        self.user = user
        self.repo_name = repo_name
        self.repo_username = repo_username
        self.__dict__.update(kwargs)

    @abstractmethod
    def _get_request_post_url(self):
        pass

    def __str__(self):
        return PR_ECHO_STRING.format(self.__dict__)

    def create(self, source, dest, reviewers, title, desc):
        "create a new pull request."
        repo = "/".join([self.user.username, self.repo_name])
        post_data = {
            'title': title,
            'description': desc,
            'close_source_branch': True,
            'reviewers': [
                {'username': username} for username in reviewers],
            'destination': {
                'branch': {'name': dest}},
            'source': {
                'branch': {'name': source},
                'repository': {'full_name': repo}},
        }
        logger.info(post_data)
        resp = requests.post(self._get_request_post_url(),
                             auth=self.user.auth,
                             json=post_data)
        logger.info(resp.status_code)
        return resp

    def list_all(self):
        """Get all open pullrequests.
        TODO Turn page
        TODO -a=all prs
        :return pullrequest_list: PullReuqest lists"""
        resp = requests.get(self.pullrequests_url, auth=user_auth)
        if resp.status_code != 200:
            raise Exception("ERROR! status_code={}, response={}".format(resp.status_code, resp.content))
        json_content = resp.json()
        logger.debug("Resp: {}".format(json.dumps(json_content, indent=2, sort_keys=True)))
        pullrequest_list = []
        pullrequest_values = json_content['values']
        for value in pullrequest_values:
            pullrequest_list.append(
                PullRequest(self.user,
                            self.repo_name,
                            id=value['id'],
                            source=value['source']['branch']['name'],
                            dest=value['destination']['branch']['name'],
                            title=value['title'],
                            author=value['author']['username'],
                            last_update=arrow.get(value['updated_on']).humanize())
            )
        return pullrequest_list

    @abstractmethod
    def _get_request_activity_url(self):
        pass

    @abstractmethod
    def _handle_activity_response(self, resp):
        "handle resp, return activity list"
        pass

    @abstractmethod
    def to_post_data(self):
        "return for request posting"
        pass

    def activities(self):
        # TODO turn page use next
        # TODO staticmethod
        # TODO more pretty return values
        resp = requests.get(self._get_request_activity_url(), auth=self.user.auth).json()
        return self._handle_activity_response(resp)

    @abstractmethod
    def submit(self):
        "Submit this pr to remote."
        pass


class Remote(object):
    "Define a remote's behavior, like submit a pr, or check activities."
    def list_all_prs(self):
        pass

    def submit_new_pr(self, pr):
        pass