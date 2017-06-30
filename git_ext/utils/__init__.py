# -*- coding: utf-8 -*-

import logging
import os
import yaml

logging.basicConfig(level=logging.DEBUG, format='%(name)s\t - %(message)s')

logger = logging.getLogger(__name__)

def read_config():
    config_file_path = os.path.join(os.path.expanduser('~'), '.git_ext.yml')
    with open(config_file_path) as config_file:
        config = yaml.load(config_file)
    return config
