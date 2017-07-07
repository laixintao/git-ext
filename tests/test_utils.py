# -*- coding: utf-8
# pylint: disable=no-self-use, invalid-name

import unittest
import mock
from utils import open_file


class GitExtUtilsTest(unittest.TestCase):

    @mock.patch('git_ext.utils.get_reviewers_group')
    def test_check_reviewers_group_without_group(self, mock_get_reviewers_group):
        mock_get_reviewers_group.return_value = {
            'yorg': ['youranl', 'dushujun', 'Jianhao', 'mrluanma', 'alpha7happy', 'kiwiz01', 'NLEI', 'lushenglv']}
        from git_ext.utils import check_reviewers_group
        raw_reviewers = "@foo @bar @hello"
        final_reviewers = check_reviewers_group(raw_reviewers)
        assert final_reviewers == ['foo', 'bar', 'hello']
