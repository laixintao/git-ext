# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import re
import commands
import shutil
from git_ext.utils import logging, read_config, make_start_with_hashtag


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

def get_commit_editmsg_bak_abs_path():
    back_commit_file_path = os.path.join(get_dotgit_abs_path(), 'COMMIT_EDITMSG.get_ext.bak')
    return back_commit_file_path


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

def init_commit_editmsg_file(source_branch, destination_branch):
    # TODO git commiting colorscheme
    # see also: https://github.com/vim/vim/blob/master/runtime/syntax/gitcommit.vim
    if os.path.isfile(get_commit_editmsg_bak_abs_path()):
        restore_commit_file()
    else:
        init_commit_template(source_branch, destination_branch)
    return get_commit_editmsg_abs_path()

def init_commit_template(source_branch, destination_branch):
    with open(os.path.join(SCRIPT_PATH, DEFAULT_PR_TEMPLATE_PATH), 'r') as template:
        with open(get_commit_editmsg_abs_path(), 'w') as commit_edit_msg:
            template_content = template.read()
            commit_log = commands.getoutput("git log --branches --not {} --pretty=format:' %h: %s'".format(destination_branch))
            diff_stat = commands.getoutput("git diff {} --stat".format(destination_branch))
            template_content = template_content.format(source_branch=source_branch,
                destination_branch=destination_branch,
                COMMIT_LOG=make_start_with_hashtag(commit_log),
                DIFF_STAT=make_start_with_hashtag(diff_stat))
            commit_edit_msg.write(template_content)
    


def backup_commit_file():
    shutil.copy2(get_commit_editmsg_abs_path(), get_commit_editmsg_bak_abs_path())

def restore_commit_file():
    shutil.copy2(get_commit_editmsg_bak_abs_path(), get_commit_editmsg_abs_path())


def read_commit_editmsg_file(pr_submit_file):
    with open(pr_submit_file, 'r') as commit_file:
        lines = commit_file.readlines()
        lines = [line for line in lines if not line.startswith('#')]
        logger.info(lines)
        # if all lines are empty, abort pr
        for line in lines:
            if line.strip():
                break
        else:
            return "", ""
        title = lines[0]
        desc = "".join(lines[1:])
    return title, desc
