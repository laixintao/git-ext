# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
import os
import codecs


class GitTestCase(unittest.TestCase):
    def setUp(self):
        self.test_git_ext_path = os.getenv("TEST_GIT_PATH")
        os.chdir(self.test_git_ext_path)

    def test_get_repo_abs_path(self):
        from git_ext.git import get_repo_abspath

        assert os.getcwd() == get_repo_abspath()

    def test_dotgit_abs_path(self):
        from git_ext.git import get_dotgit_abs_path

        assert os.getcwd() + "/.git" == get_dotgit_abs_path()

    def test_commit_editmsg_abs_path(self):
        from git_ext.git import get_commit_editmsg_abs_path

        assert os.getcwd() + "/.git/COMMIT_EDITMSG" == get_commit_editmsg_abs_path()

    def test_commit_editmsg_bak_abs_path(self):
        from git_ext.git import get_commit_editmsg_bak_abs_path

        assert (
            os.getcwd() + "/.git/COMMIT_EDITMSG.git_ext.bak"
            == get_commit_editmsg_bak_abs_path()
        )


def test_init_git_template_has_chinese(chinese_branch):
    from git_ext.git import init_commit_template
    from git_ext.git import get_repo_abspath

    assert chinese_branch == 0
    init_commit_template("test_chinese", "master")
    with codecs.open(
        get_repo_abspath() + "/.git/COMMIT_EDITMSG", encoding="utf-8"
    ) as commit_file:
        assert "提交一次中文" in commit_file.read()
