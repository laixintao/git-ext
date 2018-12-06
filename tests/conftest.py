# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import pytest

import subprocess

NEW_BRANCK_COMMAND = """
cd $TEST_GIT_PATH && 
git checkout master &&
git checkout -b test_chinese &&
echo "测试中文分支" > chinese.txt &&
git add -A &&
git commit -a -m "提交一次中文message"
"""

CLEAN_BRANCH_COMMAND = """
cd $TEST_GIT_PATH && 
git checkout master &&
git branch -D test_chinese
"""


@pytest.fixture(scope="function")
def chinese_branch():
    status = subprocess.check_call(NEW_BRANCK_COMMAND, shell=True)
    yield status
    assert subprocess.check_call(CLEAN_BRANCH_COMMAND, shell=True) == 0
