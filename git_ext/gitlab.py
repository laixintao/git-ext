import requests

from git_ext import Remote
from git_ext.utils import get_config


class GitlabRemote(Remote):
    PULL_REQUESTS_URL = "{domain}/api/v3/projects/{repo}/merge_requests"

    def __init__(self):
        super().__init__()
        # init auth header
        config = get_config()
        token = config["gitlab"]["private_token"]
        domain = config["gitlab"]["domain"]

        self.session = requests.Session()
        self.session.headers = {"PRIVATE-TOKEN": token}
        self.repo_id = f"{self.repo_username}%2F{self.repo_name}"
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
        print(resp.json())
        return resp
