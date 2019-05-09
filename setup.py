#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
# from hooks4git.scripts import Post_install
import codecs
from os import path
from pipfile import Pipfile

here = path.abspath(path.dirname(__file__))
with codecs.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get the requirements from the Pipfile
parsed = Pipfile.load(filename="Pipfile")
requirements = list(parsed.data['default'].keys())
requirements_dev = list(parsed.data['develop'].keys())

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
        'dev': requirements_dev
    },
    entry_points={
        'console_scripts': ['hooks4git=hooks4git.app:run'],
    },
    zip_safe=True
)
