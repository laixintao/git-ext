# -*- coding: utf-8 -*-

from git_ext import PullRequest
from git_ext.bitbucket import urls
from git_ext import Activity
from git_ext.utils import logging

logger = logging.getLogger(__name__)


class BitbucketPullRequest(PullRequest):
    def __init__(self, *args, **kwargs):
        super(PullRequest, self).__init__(*args, **kwargs)

    def _get_request_post_url(self):
        return urls.PULLREQUESTS.format(
            username=self.repo_username,
            repo_slug=self.repo_slug
        )

    def _get_request_activity_url(self):
        return urls.PULLREQUEST_ID_ACTIVITY.format(
            username=self.repo_username,
            repo_slug=self.repo_name,
            pull_request_id=self.id
        )

    def _handle_activity_response(self, resp):
        activities = []
        for activity in resp['values']:
            if 'comment' in activity:
                activities.append(
                    Activity(activity['comment']['user']['username'],
                             activity['comment']['content']['raw'],
                             Activity.COMMENT_TYPE,
                             activity['comment']['created_on']
                             )
                )
            elif 'update' in activity:
                activities.append(
                    Activity(activity['update']['author']['username'],
                             '[' + activity['update']['state'] + ']' + activity['update']['title'],
                             Activity.UPDATE_TYPE,
                             activity['update']['date']
                             )
                )
            elif 'approval' in activity:
                activities.append(
                    Activity(activity['update']['author']['username'],
                             "Nice Work",
                             Activity.UPDATE_TYPE,
                             activity['update']['date']
                             )
                )
            else:
                logger.info(activity)
        activities.reverse()  # sorted by time
        return activities