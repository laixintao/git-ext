# -*- coding: utf-8 -*-

from __future__ import absolute_import

from requests.auth import HTTPBasicAuth
from git_ext.utils import get_config
from git_ext.utils import logging

logger = logging.getLogger(__name__)

config = get_config()
user_email = config['bitbucket']['email']
user_password = config['bitbucket']['password']

logger.debug("User loaded from yaml - {}:{}".format(user_email, user_password))
user_auth = HTTPBasicAuth(user_email, user_password)
