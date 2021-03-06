# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.hook import hook_it
import os


class HookHookItTestCase(BaseTestCase):
    def test_add_precommit_successfully(self):
        action = hook_it(BaseTestCase.tmp_valid_path)
        self.assertTrue(action)
        action = hook_it(BaseTestCase.tmp_valid_path)
        self.assertTrue(action)
        precommit_path = os.path.join(BaseTestCase.tmp_valid_git_path, "hooks/pre-commit")
        self.assertTrue(os.path.isfile(precommit_path))  # noqa
