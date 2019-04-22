#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
import os


class BaseTestCase(TestCase):
    base_path = os.getcwd()
    tmp_valid_path = os.path.join(base_path, "tmp/valid")
    tmp_invalid_path = os.path.join(base_path, "tmp/invalid")
    tmp_valid_git_path = os.path.join(tmp_valid_path, ".git")
    tmp_invalid_git_path = os.path.join(tmp_invalid_path, ".git")

    def setUp(self):
        # create test temporary directory
        os.system("mkdir -p tmp/valid && cd tmp/valid && git init")  # noqa
        os.system("mkdir -p tmp/invalid && cd tmp/invalid && git init && cd .git && rm -rf hooks")  # noqa

    def tearDown(self):
        # remove all test files
        os.system("rm -r tmp/")  # noqa
