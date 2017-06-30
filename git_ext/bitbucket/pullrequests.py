# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import requests
from git_ext.bitbucket.user import user_auth
from git_ext.bitbucket import urls
from git_ext.utils import logging

logger = logging.getLogger(__name__)


class PullRequests(object):

    def __init__(self, username, repo_slug):
        self.username = username
        self.repo_slug = repo_slug
        logger.debug("username: {}, resp_slug: {}".format(
            self.username, self.repo_slug))
        self.pullrequests_url = urls.PULLREQUESTS.format(
            username=self.username,
            repo_slug=self.repo_slug)
        self.pullrequests = []
        self.is_requests_updated = False

    def update_pullrequests(self):
        "Only open prs by default"
        resp = requests.get(self.pullrequests_url, auth=user_auth).json()
        logger.debug("Resp: {}".format(json.dumps(resp, indent=4, sort_keys=True)))
        # TODO Turn page
        return resp['values']

    def create(self, source, dest, reviewers, title, desc):
        repo = "/".join([self.username, self.repo_slug])
        post_data = {
            'title': title,
            'description': desc,
            'close_source_branch': True,
            'reviewers':[
                {'username': username} for username in reviewers],
            'destination': {
                'branch': {'name': dest}},
            'source': {
                'branch': {'name': source},
                'repository': {'full_name': repo}},
        }
        logger.info(post_data)
        resp = requests.post(urls.PULLREQUESTS.format(username=self.username, repo_slug=self.repo_slug),
                             auth=user_auth,
                             json=post_data)
        logger.info(resp.status_code)
        logger.info(resp.json())

    def pullrequests_list(self):
        if not self.is_requests_updated:
            self.update_pullrequests()
        return [(pr['id'], pr['title'], pr['author']['username'], pr['created_on']) for pr in self.pullrequests]

    def pullrequests_activity(self, pr_id):
        # TODO turn page use next
        # TODO staticmethod
        resp = requests.get(urls.PULLREQUEST_ID_ACTIVITY.format(
            username=self.username,
            repo_slug=self.repo_slug,
            pull_request_id=pr_id), auth=user_auth).json()
        activities = []
        for activity in resp['values']:
            if 'comment' in activity:
                activities.append(('commented on',
                                   activity['comment']['created_on'],
                                   activity['comment']['user']['username'],
                                   activity['comment']['content']['raw'],))
            elif 'update' in activity:
                activities.append(('updated',
                                   activity['update']['date'],
                                   activity['update']['author']['username'],
                                   '[' + activity['update']['state'] + ']' + activity['update']['title']))
            elif 'approval' in activity:
                activities.append(('approved',
                                   activity['approval']['date'],
                                   activity['approval']['user']['username'],
                                   "Nice work!"))
            else:
                logger.info(activity)
        return activities


if __name__ == '__main__':
    pr = PullRequests('deepanalyzer', 'yorg')
    logger.info(pr.pullrequests_list())
