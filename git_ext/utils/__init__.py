# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os
import commands
import yaml

config = None
logger = logging.getLogger(__name__)

def read_config():
    global config
    config_file_path = os.path.join(os.path.expanduser('~'), '.git_ext.yml')
    if config:
        return config
    with open(config_file_path) as config_file:
        config = yaml.load(config_file)
    return config

def get_gitext_config():
    config_file = read_config()
    gitext_config = config_file.get('git_ext')
    return gitext_config

def config_log():
    if os.getenv('GITEXT') == 'debug':
        level = logging.DEBUG
    else:
        level = logging.ERROR
    logging.basicConfig(level=level, format='%(name)s\t - %(message)s')

def get_reviewers_group():
    "Return group defined in ~/.git_ext.yml, for quick input reviewers."
    config = read_config()
    return config.get('reviewers_group')

def check_reviewers_group(raw_reviewers):
    reviewers_group = get_reviewers_group()
    splited_reviewers = "".join(raw_reviewers.split()).split('@')[1:]  # why there is a space??
    final_reviewers = []
    logger.info("reviewers_group: {}".format(reviewers_group))
    for reviewer in splited_reviewers:
        if reviewer in reviewers_group:
            final_reviewers.extend(reviewers_group[reviewer])
        else:
            final_reviewers.append(reviewer)
    return final_reviewers

config_log()
read_config()
