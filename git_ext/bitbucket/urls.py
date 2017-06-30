# -*- coding: utf-8 -*-

BASE = 'https://api.bitbucket.org'
PULLREQUESTS = BASE + '/2.0/repositories/{username}/{repo_slug}/pullrequests'
PULLREQUESTS_ACTIVITY = BASE + '/2.0/repositories/{username}/{repo_slug}/pullrequests/activity'
PULLREQUEST_ID_ACTIVITY = BASE + '/2.0/repositories/{username}/{repo_slug}/pullrequests/{pull_request_id}/activity'
