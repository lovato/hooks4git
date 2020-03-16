# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.console import Display
from hooks4git.tools import get_dash


class DividerTestCase(BaseTestCase):
    def test_divider(self):
        d = Display()
        dash = get_dash()
        response = d.divider()
        self.assertTrue(dash in response)
        self.assertTrue(len(response) == 91)
