# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git import tools
import sys


class UserSiteTestCase(BaseTestCase):
    display = None

    def test_usersite(self):
        path = tools.add_usersitepackages_to_path("python")
        self.assertEqual(path, sys.path[0])
