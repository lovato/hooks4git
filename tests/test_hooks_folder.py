#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import BaseTestCase
from hooks4git.scripts import get_hooks_path


class HooksFolderTestCase(BaseTestCase):
    def test_get_hooks_path_missing_folder_notcreate(self):
        path = get_hooks_path("/tmp", create_if_missing=False)
        self.assertTrue(path is None)

    def test_get_hooks_path_missing_folder_create(self):
        path = get_hooks_path("/tmp", create_if_missing=True)
        self.assertTrue(path is None)

    def test_get_hooks_path_valid_folder_notcreate(self):
        path = get_hooks_path(BaseTestCase.tmp_valid_git_path, create_if_missing=False)
        self.assertTrue(path is not None)

    def test_get_hooks_path_valid_folder_create(self):
        path = get_hooks_path(BaseTestCase.tmp_valid_git_path, create_if_missing=True)
        self.assertTrue(path is not None)

    def test_get_hooks_path_invalid_folder_notcreate(self):
        path = get_hooks_path(BaseTestCase.tmp_invalid_git_path, create_if_missing=False)
        self.assertTrue(path is None)

    def test_get_hooks_path_invalid_folder_create(self):
        path = get_hooks_path(BaseTestCase.tmp_invalid_git_path, create_if_missing=True)
        self.assertTrue(path is not None)
