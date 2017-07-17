# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os
import yaml

logger = logging.getLogger(__name__)


def get_config():
    config_file_path = os.path.join(os.path.expanduser('~'), '.git_ext.yml')
    with open(config_file_path) as config_file:
        config = yaml.load(config_file)
    return config


def get_reviewers_group():
    "Return group defined in ~/.git_ext.yml, for quick input reviewers."
    config = get_config()
    return config.get('reviewers_group')


def check_reviewers_group(raw_reviewers):
    reviewers_group = get_reviewers_group()
    logger.info(reviewers_group)
    splited_reviewers = [reviewer for reviewer in "".join(raw_reviewers.split()).split('@') if reviewer]
    final_reviewers = []
    logger.info("reviewers_group: {}".format(reviewers_group))
    for reviewer in splited_reviewers:
        if reviewer in reviewers_group:
            final_reviewers.extend(reviewers_group[reviewer])
        else:
            final_reviewers.append(reviewer)
    return final_reviewers

def config_log():
    if os.getenv('GITEXT') == 'debug':
        level = logging.DEBUG
    else:
        level = logging.ERROR
        logging.basicConfig(level=level, format='%(name)s\t - %(message)s')


def make_start_with_hashtag(raw_content):
    # FIXME not test in windows
    lines = raw_content.split(os.linesep)
    result = ""
    logger.info("lines")
    for line in lines[:-1]:
        logger.info(line)
        if not line.strip(): continue
        result = result + '#' + line + os.linesep
    result = result + '#' + lines[-1]  # no linesep in last line
    return result

config_log()
