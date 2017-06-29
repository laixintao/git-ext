# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
from git_ext.bitbucket import urls, user_email, user_password

resp = requests.get('https://api.bitbucket.org/2.0/repositories/deepanalyzer/yorg/commits/',
                    auth=(user_email, user_password))

