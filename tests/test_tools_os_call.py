# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.tools import os_call


class OsCallTestCase(BaseTestCase):
    def test_os_call_invalid(self):
        response = os_call("/bin/eecho")
        self.assertTupleEqual(response, (127, "", "/bin/bash: /bin/eecho: No such file or directory\n"))

    def test_os_call_valid(self):
        response = os_call("/bin/echo success")
        self.assertTupleEqual(response, (0, "success\n", ""))
