#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import BaseTestCase
from hooks4git.scripts import Exec
import os


class PreCommitTestCase(BaseTestCase):

    def test_add_precommit_successfully(self):
        action = Exec.add_hooks(BaseTestCase.tmp_valid_path)
        self.assertTrue(action)
        precommit_path = os.path.join(BaseTestCase.tmp_valid_git_path, "hooks/pre-commit")
        self.assertTrue(os.path.isfile(precommit_path))  # noqa
