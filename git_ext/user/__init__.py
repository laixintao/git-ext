# -*- encoding: utf-8 -*-

from requests.auth import HTTPBasicAuth

class User(object):
    
    def __init__(username, password):
        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(self.username, self.password)
