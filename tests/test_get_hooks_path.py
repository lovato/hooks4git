# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.tools import get_hooks_path


class HooksFolderTestCase(BaseTestCase):
    def test_get_hooks_path_missing_folder(self):
        path = get_hooks_path("/tmp")
        self.assertTrue(path is None)

    def test_get_hooks_path_valid_folder(self):
        path = get_hooks_path(BaseTestCase.tmp_valid_git_path)
        self.assertTrue(path is not None)

    def test_get_hooks_path_invalid_folder(self):
        path = get_hooks_path(BaseTestCase.tmp_invalid_git_path)
        self.assertTrue(path is not None)
