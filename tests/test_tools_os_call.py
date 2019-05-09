# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.tools import os_call


class OsCallTestCase(BaseTestCase):
    def test_os_call_invalid(self):
        response = os_call("/bin/eecho")
        self.assertTrue(response == (-1, "", ""))

    def test_os_call_valid(self):
        response = os_call("/bin/echo", "success")
        self.assertTrue(response == (0, "success\n", ""))
