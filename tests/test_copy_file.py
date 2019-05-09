# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.tools import copy_file
import os


class HooksFolderTestCase(BaseTestCase):
    def test_copy_file_source_invalid(self):
        flag = copy_file(
            os.path.join(BaseTestCase.tmp_path, "invalid_file"),
            os.path.join(BaseTestCase.tmp_path, "invalid_file_copy"),
        )  # noqa
        self.assertTrue(flag is False)

    def test_copy_file_destination_invalid(self):
        flag = copy_file(os.path.join(BaseTestCase.tmp_path, "invalid_file"), "/invalid_file_copy")  # noqa
        self.assertTrue(flag is False)

    def test_copy_file_both_valid(self):
        flag = copy_file(
            os.path.join(BaseTestCase.tmp_path, "valid_file"), os.path.join(BaseTestCase.tmp_path, "valid_file_copy")
        )  # noqa
        self.assertTrue(flag is True)
