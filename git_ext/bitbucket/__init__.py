# -*- coding: utf-8 -*-

from git_ext import config
from git_ext.utils import logging

logger = logging.getLogger(__name__)

user_email = config['bitbucket']['email']
user_password = config['bitbucket']['password']

logger.debug("{}: {}".format(user_email, user_password))
