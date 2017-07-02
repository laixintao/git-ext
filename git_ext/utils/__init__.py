# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os
import commands
import yaml


def read_config():
    config_file_path = os.path.join(os.path.expanduser('~'), '.git_ext.yml')
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


config_log()
