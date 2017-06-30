# -*- coding: utf-8 -*-

import logging
import os
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
    gitext_config = get_gitext_config()
    if not gitext_config:
        return
    logging_config = gitext_config.get('logging')
    if logging_config:
        logging.basicConfig(level=logging_config.get('level'),
                            format=logging_config.get('format'))
    else:
        logging.basicConfig(level=logging.ERROR, format='%(name)s\t - %(message)s')

config_log()
