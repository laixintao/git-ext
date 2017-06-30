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
        logger.debug(urls.PULLREQUESTS)
        self.pullrequests_url = urls.PULLREQUESTS.format(
            username=self.username,
            repo_slug=self.repo_slug)
        self.pullrequests = self.update_pullrequests()

    def update_pullrequests(self):
        "Only open prs by default"
        resp = requests.get(self.pullrequests_url, auth=user_auth).json()
        logger.debug("Resp: {}".format(json.dumps(resp, indent=4, sort_keys=True)))
        # TODO Turn page
        return resp['values']

    def pullrequests_list(self):
        return [(pr['id'], pr['title']) for pr in self.pullrequests]


if __name__ == '__main__':
    pr = PullRequests('deepanalyzer', 'yorg')
    logger.info(pr.pullrequests_list())
