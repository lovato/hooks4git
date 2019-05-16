# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git import hook
import time
import datetime
from hooks4git.console import Display


class HookReportTestCase(BaseTestCase):
    display = None

    def test_report(self):
        self.display = Display(False)
        self._test(2, 1, "was")
        self._test(1, 3, "were")

    def _test(self, delay, steps, verb):
        hook.steps_executed = steps
        start_time = datetime.datetime.now()
        time.sleep(delay)
        line1, line2 = hook.report(start_time, self.display)
        self.assertEqual(line1, "STEPS| %s %s executed" % (hook.steps_executed, verb))
        expected_line2 = "TIME | Execution took 0:00:%02d." % delay
        self.assertEqual(line2[:30], expected_line2)
