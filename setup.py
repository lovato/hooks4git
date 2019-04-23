#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
# from hooks4git.scripts import Post_install
import codecs
from os import path

here = path.abspath(path.dirname(__file__))
with codecs.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get the requirements from the requirements.txt file
with codecs.open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read()

try:
    # Get the dev requirements from the requirements-dev.txt file
    with codecs.open(path.join(here, 'requirements-dev.txt'), encoding='utf-8') as f:
        requirements_dev = f.read()
except:  # noqa
    # It is ok, this file only exists when developing this package, not when installing.
    requirements_dev = ''

project_name = 'hooks4git'
__version__ = __import__(project_name).__version__
__author__ = __import__(project_name).__author__
__author_email__ = __import__(project_name).__author_email__
__author_username__ = __import__(project_name).__author_username__
__description__ = __import__(project_name).__description__

setup(
    name=project_name,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    download_url='https://github.com/{}/{}/tarball/{}'.format(__author_username__, project_name, __version__),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    url="https://github.com/lovato/hooks4git",
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    platforms=['any'],
    extras_require={
        'dev': [requirements_dev.split('\n')]
    },
    scripts=["hooks4git/hooks4git"],
    zip_safe=True
)
