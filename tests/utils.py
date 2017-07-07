# -*- coding: utf-8 -*-

import os

def read_file(path):
    "read file from fixtures, return file content"
    with open(os.path.abspath("tests/fixtures/"+path), 'r') as open_file:
        file_content = open_file.read()
    return file_content

def open_file(path):
    return open(os.path.abspath("tests/fixtures/"+path), 'r')
