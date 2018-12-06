# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class Gist(object):
    post_url = "https://api.github.com/gists"
    patch_url = "https://api.github.com/gists/{id}"

    def __init__(self, file_path, description="", is_public=False, user=None):
        self.file_path = file_path
        self.description = description
        self.is_public = is_public
        self.user = user
        with open(self.file_path, "r") as gist_file:
            self.content = gist_file.read()

    def submit(self):
        "Submit gist to github."
