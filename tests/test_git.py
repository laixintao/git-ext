# -*- coding: utf-8 -*-

import unittest
import os

class GitTestCase(unittest.TestCase):
    def setUp(self):
        self.test_git_ext_path = os.getenv('TEST_GIT_PATH')
        os.chdir(self.test_git_ext_path)

    def test_get_repo_abs_path(self):
        from git_ext.git import get_repo_abspath
        assert os.getcwd() == get_repo_abspath()

    def test_dotgit_abs_path(self):
        from git_ext.git import get_dotgit_abs_path
        assert os.getcwd() + '/.git' == get_dotgit_abs_path()

    def test_commit_editmsg_abs_path(self):
        from git_ext.git import get_commit_editmsg_abs_path
        assert os.getcwd() + '/.git/COMMIT_EDITMSG' == get_commit_editmsg_abs_path()

    def test_commit_editmsg_bak_abs_path(self):
        from git_ext.git import get_commit_editmsg_bak_abs_path
        assert os.getcwd() + '/.git/COMMIT_EDITMSG.git_ext.bak' == get_commit_editmsg_bak_abs_path()
