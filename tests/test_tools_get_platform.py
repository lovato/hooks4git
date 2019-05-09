# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.tools import get_platform


class GetPlatformTestCase(BaseTestCase):
    def test_get_platform_invalid(self):
        platform = get_platform("FakeOS", {})
        self.assertTrue(platform == "FakeOS")

    def test_get_platform_valid(self):
        platform = get_platform("linux", {})
        self.assertTrue(platform == "Linux")
        platform = get_platform("linux1", {})
        self.assertTrue(platform == "Linux")
        platform = get_platform("linux2", {})
        self.assertTrue(platform == "Linux")
        platform = get_platform("darwin", {})
        self.assertTrue(platform == "Mac")
        platform = get_platform("win32", {})
        self.assertTrue(platform == "Windows")
        platform = get_platform("win32", {"MSYSTEM": "MINGW64"})
        self.assertTrue(platform == "WindowsGitBash")
