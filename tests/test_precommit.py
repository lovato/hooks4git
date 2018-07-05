#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import BaseTestCase
from hooks4git.scripts import Exec
import os


class PreCommitTestCase(BaseTestCase):

    def test_add_precommit_successfully(self):
        action = Exec.add_pre_commit(os.path.join(os.getcwd(), "tmp"))
        self.assertTrue(action)

    def test_add_precommit_successfully_2(self):
        action = Exec.add_pre_commit(os.path.join(os.getcwd(), "tmp"))
        self.assertTrue(action)
        self.assertTrue(os.path.isfile("tmp/.git/hooks/pre-commit"))
