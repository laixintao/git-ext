# -*- coding: utf-8
# pylint: disable=no-self-use, invalid-name

from __future__ import unicode_literals

import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import os


class GitExtUtilsTest(unittest.TestCase):
    @mock.patch("git_ext.utils.get_reviewers_group")
    def test_check_reviewers_group_without_group(self, mock_get_reviewers_group):
        mock_get_reviewers_group.return_value = {
            "yorg": [
                "youranl",
                "dushujun",
                "Jianhao",
                "mrluanma",
                "alpha7happy",
                "kiwiz01",
                "NLEI",
                "lushenglv",
            ]
        }
        from git_ext.utils import check_reviewers_group

        raw_reviewers = "@foo @bar @hello"
        final_reviewers = check_reviewers_group(raw_reviewers)
        assert final_reviewers == ["foo", "bar", "hello"]

    @mock.patch("git_ext.utils.get_reviewers_group")
    def test_check_reviewers_group_with_group(self, mock_get_reviewers_group):
        mock_get_reviewers_group.return_value = {
            "yorg": ["youranl", "dushujun", "Jianhao", "mrluanma"]
        }
        from git_ext.utils import check_reviewers_group

        raw_reviewers = "@yorg @bar @hello"
        final_reviewers = check_reviewers_group(raw_reviewers)
        assert final_reviewers == [
            "youranl",
            "dushujun",
            "Jianhao",
            "mrluanma",
            "bar",
            "hello",
        ]

    @mock.patch("git_ext.utils.get_reviewers_group")
    def test_check_reviewers_group_with_group_only(self, mock_get_reviewers_group):
        mock_get_reviewers_group.return_value = {
            "yorg": ["youranl", "dushujun", "Jianhao", "mrluanma"]
        }
        from git_ext.utils import check_reviewers_group

        raw_reviewers = "@yorg"
        final_reviewers = check_reviewers_group(raw_reviewers)
        assert final_reviewers == ["youranl", "dushujun", "Jianhao", "mrluanma"]

    def test_get_config_success(self):
        from git_ext.utils import get_config

        config = get_config()
        assert config["bitbucket"]["email"]
        assert config["bitbucket"]["password"]

    @mock.patch.dict(os.environ, {"GITEXT": "debug"})
    @mock.patch("logging.basicConfig")
    def test_config_log_debug(self, mock_logging):
        from git_ext.utils import config_log
        import logging

        config_log()
        mock_logging.assert_called_with(
            level=logging.DEBUG, format="%(name)s\t - %(message)s"
        )

    def test_make_start_with_hashtag(self):
        raw_str = "hello, this is\ntest for\nhashtag..."
        from git_ext.utils import make_start_with_hashtag

        result = make_start_with_hashtag(raw_str)
        assert result == "#hello, this is\n#test for\n#hashtag..."
