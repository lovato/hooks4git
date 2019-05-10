# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.console import Display


class DividerTestCase(BaseTestCase):
    def test_divider(self):
        d = Display()
        check = "CHECK"

        response = d.say("PASS", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 43)

        response = d.say("PASS ", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 43)

        response = d.say("FAIL", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 47)

        response = d.say("FAIL ", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 43)

        response = d.say("SOUT", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 32)

        response = d.say("SERR", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 32)

        response = d.say("INFO", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 38)

        response = d.say("WARN", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 38)

        response = d.say("STEP", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 38)

        response = d.say("STEPS", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 38)

        response = d.say("TIME", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 38)

        response = d.say("ERR!", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 38)

        response = d.say("TITLE", check)
        self.assertTrue(check in response)
        self.assertTrue(len(response) == 26)
