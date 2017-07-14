# -*- coding: utf-8
# pylint: disable=no-self-use, invalid-name

import unittest
import mock


class GitExtUtilsTest(unittest.TestCase):

    @mock.patch('git_ext.utils.get_reviewers_group')
    def test_check_reviewers_group_without_group(self, mock_get_reviewers_group):
        mock_get_reviewers_group.return_value = {
            'yorg': ['youranl', 'dushujun', 'Jianhao', 'mrluanma', 'alpha7happy', 'kiwiz01', 'NLEI', 'lushenglv']}
        from git_ext.utils import check_reviewers_group
        raw_reviewers = "@foo @bar @hello"
        final_reviewers = check_reviewers_group(raw_reviewers)
        assert final_reviewers == ['foo', 'bar', 'hello']

    @mock.patch('git_ext.utils.get_reviewers_group')
    def test_check_reviewers_group_with_group(self, mock_get_reviewers_group):
        mock_get_reviewers_group.return_value = {
            'yorg': ['youranl', 'dushujun', 'Jianhao', 'mrluanma']}
        from git_ext.utils import check_reviewers_group
        raw_reviewers = "@yorg @bar @hello"
        final_reviewers = check_reviewers_group(raw_reviewers)
        assert final_reviewers == ['youranl', 'dushujun', 'Jianhao', 'mrluanma', 'bar', 'hello']

    @mock.patch('git_ext.utils.get_reviewers_group')
    def test_check_reviewers_group_with_group_only(self, mock_get_reviewers_group):
        mock_get_reviewers_group.return_value = {
            'yorg': ['youranl', 'dushujun', 'Jianhao', 'mrluanma']}
        from git_ext.utils import check_reviewers_group
        raw_reviewers = "@yorg"
        final_reviewers = check_reviewers_group(raw_reviewers)
        assert final_reviewers == ['youranl', 'dushujun', 'Jianhao', 'mrluanma']

    def test_get_config_success(self):
        from git_ext.utils import config
        assert config['bitbucket']['email']
        assert config['bitbucket']['password']

    def test_config_log_no_debug(self):
        import os
        os.environ['GITEXT'] = ""
        from git_ext.utils import logging, config_log
        config_log()
        assert logging.getLogger().getEffectiveLevel() == logging.ERROR
        os.environ['GITEXT'] = ""

    def test_config_log_debug(self):
        import os
        os.environ['GITEXT'] = 'debug'
        from git_ext.utils import logging
        assert logging.getLogger().getEffectiveLevel() == logging.ERROR
        os.environ['GITEXT'] = ""
