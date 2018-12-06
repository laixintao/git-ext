# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import requests

from git_ext import PullRequest, Remote
from git_ext import Activity, User
from git_ext.utils import logging
from git_ext.utils import get_config

logger = logging.getLogger(__name__)


def get_bitbucket_user():
    config = get_config()
    user_email = config["bitbucket"]["email"]
    user_password = config["bitbucket"]["password"]
    return User(user_email, user_password)


class BitbucketRemote(Remote):
    BASE = "https://api.bitbucket.org"
    PULLREQUESTS = BASE + "/2.0/repositories/{username}/{repo_slug}/pullrequests"
    ACTIVITY = BASE + "/2.0/repositories/{username}/{repo_slug}/pullrequests/activity"
    ACTIVITY_DETAIL = (
        BASE
        + "/2.0/repositories/{username}/{repo_slug}/pullrequests/{pull_request_id}/activity"
    )
    PR_URL = "https://bitbucket.org/{username}/{repo_slug}/pull-requests/{_id}"

    def __init__(self):
        super(BitbucketRemote, self).__init__(get_bitbucket_user())
        self.pull_requests_url = self.PULLREQUESTS.format(
            username=self.repo_username, repo_slug=self.repo_name
        )

    def get_all_pullrequests(self):
        resp = requests.get(self.pull_requests_url, auth=self.user.auth)
        if resp.status_code != 200:
            raise Exception(
                "ERROR! status_code={}, response={}".format(
                    resp.status_code, resp.content
                )
            )
        json_content = resp.json()
        logger.debug(
            "Resp: {}".format(json.dumps(json_content, indent=2, sort_keys=True))
        )
        pullrequest_list = []
        pullrequest_values = json_content["values"]
        for value in pullrequest_values:
            pullrequest_list.append(
                PullRequest(
                    value["id"],
                    value["source"]["branch"]["name"],
                    value["destination"]["branch"]["name"],
                    value["author"]["username"],
                    [],  # no reviewers
                    value["title"],
                    value["description"],
                )
            )
        return pullrequest_list

    def submit_new_pr(self, pr):
        repository_full_name = "/".join([self.repo_username, self.repo_name])
        post_data = {
            "title": pr.title,
            "description": pr.description,
            "close_source_branch": True,
            "reviewers": [{"username": username} for username in pr.reviewers],
            "destination": {"branch": {"name": pr.dest_branch}},
            "source": {
                "branch": {"name": pr.source_branch},
                "repository": {"full_name": repository_full_name},
            },
        }
        logger.info(post_data)
        resp = requests.post(
            self.pull_requests_url, auth=self.user.auth, json=post_data
        )
        logger.info(resp.status_code)
        logger.info(json.dumps(resp.json(), indent=2, ensure_ascii=False))
        if resp.status_code == 201 and "id" in resp.json():
            pr._id = resp.json()["id"]
            pr.pr_view_url = BitbucketRemote.PR_URL.format(
                username=self.repo_username, repo_slug=self.repo_name, _id=pr._id
            )
        else:
            print(resp.json())
            raise Exception("PR create failed")

        return resp

    def get_activities(self, pr_id):
        resp = requests.get(
            self.ACTIVITY_DETAIL.format(
                username=self.repo_username,
                repo_slug=self.repo_name,
                pull_request_id=pr_id,
            ),
            auth=self.user.auth,
        ).json()
        logger.info(resp)
        activities = []
        for activity in resp["values"]:
            if "comment" in activity:
                activities.append(
                    Activity(
                        activity["comment"]["user"]["username"],
                        activity["comment"]["content"]["raw"],
                        Activity.COMMENT_TYPE,
                        activity["comment"]["created_on"],
                    )
                )
            elif "update" in activity:
                logger.info(activity)
                activities.append(
                    Activity(
                        activity["update"]["author"]["username"],
                        "["
                        + activity["update"]["state"]
                        + "]"
                        + activity["update"]["title"],
                        Activity.UPDATE_TYPE,
                        activity["update"]["date"],
                    )
                )
            elif "approval" in activity:
                activities.append(
                    Activity(
                        activity["approval"]["user"]["username"],
                        "Nice Work",
                        Activity.UPDATE_TYPE,
                        activity["approval"]["date"],
                    )
                )
            else:
                logger.info(activity)
        activities.reverse()  # sorted by time
        return activities
