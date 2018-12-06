# -*- coding: utf-8 -*-

import unittest
import os

try:
    from unittest import mock
except ImportError:
    import mock
import json

from six.moves import input

from click.testing import CliRunner


class PullRequestTestCase(unittest.TestCase):
    def setUp(self):
        self.test_git_ext_path = os.getenv("TEST_GIT_PATH")
        os.chdir(self.test_git_ext_path)
        self.runner = CliRunner()

    @mock.patch("requests.post")
    @mock.patch("six.moves.input")
    @mock.patch("os.system")
    def test_pull_request_create(self, mock_system, mock_raw_input, mock_post):
        from git_ext.git import SCRIPT_PATH
        from git_ext.bin.pullrequest import create, get_remote
        import requests

        commit_msg_path = self.test_git_ext_path + "/.git/COMMIT_EDITMSG"

        def write_commit_msg(path):
            with open(commit_msg_path, "w") as cmt:
                cmt.write("title test\ndescription")

        mock_system.side_effect = write_commit_msg
        with open(
            os.path.join(
                SCRIPT_PATH, "../tests/fixture/create_pr_success_response.json"
            ),
            "r",
        ) as resp_file:
            resp = requests.Response()
            content = resp_file.read()
            resp.json = lambda: json.loads(content)
            resp.status_code = 201
        mock_post.return_value = resp
        obj = {"remote": get_remote()}
        result = self.runner.invoke(create, ["test_a", "master"], obj=obj)
        print(result.output)
        assert result.exit_code == 0
