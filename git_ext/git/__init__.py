# -*- coding: utf-8 -*-

import os
import re
import commands
from git_ext.utils import logging

logger = logging.getLogger(__name__)

def get_repo_abspath():
    status, repo_abspath = commands.getstatusoutput('git rev-parse --show-toplevel')
    return repo_abspath


def get_repo_slug():
    repo_abspath = get_repo_abspath()
    repo_slug = os.path.basename(repo_abspath)
    git_config = os.path.join(repo_abspath, '.git/config')
    with open(git_config, 'r') as git_config_file:
        content = git_config_file.read()
        matcher = re.search(r"git@bitbucket.org:([a-zA-Z_]+)/{}.git".format(repo_slug), content)
        username = matcher.group(1)
        logger.info("username: {}, repo_slug: {}".format(username, repo_slug))
    return username, repo_slug
