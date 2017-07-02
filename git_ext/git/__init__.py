# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import re
import commands
from git_ext.utils import logging, read_config


DEFAULT_PR_TEMPLATE_PATH = '../static/PR_SUBMIT_TEMPLATE'
SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
logger = logging.getLogger(__name__)

def get_repo_abspath():
    status, repo_abspath = commands.getstatusoutput('git rev-parse --show-toplevel')
    return repo_abspath

def get_dotgit_abs_path():
    repo_abspath = get_repo_abspath()
    return os.path.join(repo_abspath, '.git')

def get_commit_editmsg_abs_path():
    return os.path.join(get_dotgit_abs_path(), 'COMMIT_EDITMSG')

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

def init_commit_editmsg_file():
    # TODO write diff message to template file
    with open(os.path.join(SCRIPT_PATH, DEFAULT_PR_TEMPLATE_PATH), 'r') as template:
        with open(get_commit_editmsg_abs_path(), 'w') as commit_edit_msg:
            commit_edit_msg.write(template.read())
    return get_commit_editmsg_abs_path()

def read_commit_editmsg_file(pr_submit_file):
    with open(pr_submit_file, 'r') as commit_file:
        lines = commit_file.readlines()
        if not lines:
            return '', ''
        title = lines[0]
        desc = "".join(lines[1:])
    return title, desc
