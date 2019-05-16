# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git import hook
import time
import datetime
from hooks4git.console import Display


class HookReportTestCase(BaseTestCase):
    def test_report(self):
        display = Display(False)
        hook.steps_executed = 5
        delay = 2
        start_time = datetime.datetime.now()
        time.sleep(delay)
        line1, line2 = hook.report(start_time, display)
        self.assertEqual(line1, "STEPS| %s were executed" % hook.steps_executed)
        expected_line2 = "TIME | Execution took 0:00:%02d." % delay
        self.assertEqual(line2[:30], expected_line2)
