import requests
import logging

from git_ext import Remote
from git_ext.utils import get_config

logger = logging.getLogger(__name__)


class GitlabRemote(Remote):
    PULL_REQUESTS_URL = "{domain}/api/v3/projects/{repo}/merge_requests"
    PR_URL = "{domain}/{username}/{repo}/merge_requests/{_id}"

    def __init__(self):
        super().__init__()
        # init auth header
        config = get_config()
        token = config["gitlab"]["private_token"]
        domain = config["gitlab"]["domain"]

        self.session = requests.Session()
        self.session.headers = {"PRIVATE-TOKEN": token}
        self.repo_id = f"{self.repo_username}%2F{self.repo_name}"
        self.domain = domain
        self.pull_request_url = self.PULL_REQUESTS_URL.format(
            domain=domain, repo=self.repo_id
        )

    def submit_new_pr(self, pr):
        resp = self.session.post(
            self.pull_request_url,
            data={
                "id": self.repo_id,
                "source_branch": pr.source_branch,
                "target_branch": pr.dest_branch,
                "title": pr.title,
                "description": pr.description,
            },
        )
        logger.debug(resp.json())
        if resp.status_code == 201 and "iid" in resp.json():
            pr._id = resp.json()["iid"]
            pr.pr_view_url = self.PR_URL.format(
                domain=self.domain,
                username=self.repo_username,
                repo=self.repo_name,
                _id=pr._id
            )
        return resp
