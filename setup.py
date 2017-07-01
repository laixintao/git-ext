# -*- coding: utf-8 -*-

import os
import sys
from codecs import open
from setuptools import setup, find_packages

VERSION = 0.1
DESCRIPTION = 'A git extension that allows you submit pullrequests from command line.'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as f:
    readme = f.read()

with open(os.path.join(here, 'requirements.txt'), 'r') as f:
    requires = f.read()

setup(
    name='git-ext',
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme,
    author='laixintao',
    author_email='laixintao1995@163.com',
    url='https://github.com/laixintao/git-ext',
    packages=find_packages(),
    package_dir={'git_ext': 'git_ext'},
    include_package_data=True,
    install_requires=requires,
    license='GNU',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
        ),
    # TODO use install to generic yml file cmdclass={'git-pullrequests': PyTest},
    entry_points={
        'console_scripts': [
            'git-pullrequest = git_ext.bin.pullrequests',
        ],
        'gui_scripts': []
    }
)
