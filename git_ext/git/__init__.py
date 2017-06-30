# -*- coding: utf-8 -*-

import os
import re
import commands
from git_ext.utils import logging, read_config


logger = logging.getLogger(__name__)

def get_repo_abspath():
    status, repo_abspath = commands.getstatusoutput('git rev-parse --show-toplevel')
    return repo_abspath

def get_dotgit_abs_path():
    repo_abspath = get_repo_abspath()
    return os.path.join(repo_abspath, '.git')

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

def get_git_core_editor():
    editor = commands.getoutput('git config --global core.editor')
    logger.debug("Core editor: {}".format(editor))
    return editor
