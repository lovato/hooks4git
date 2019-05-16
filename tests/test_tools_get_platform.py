# -*- coding: utf-8 -*-
from tests import BaseTestCase
from hooks4git.tools import get_platform
import mock


class GetPlatformTestCase(BaseTestCase):
    @mock.patch("sys.platform", "FakeOS")
    def test_get_platform_invalid(self):
        platform = get_platform()
        self.assertTrue(platform == "FakeOS")

    @mock.patch("sys.platform", "linux")
    def test_get_platform_linux(self):
        platform = get_platform()
        self.assertTrue(platform == "Linux")

    @mock.patch("sys.platform", "linux1")
    def test_get_platform_linux1(self):
        platform = get_platform()
        self.assertTrue(platform == "Linux")

    @mock.patch("sys.platform", "linux2")
    def test_get_platform_linux2(self):
        platform = get_platform()
        self.assertTrue(platform == "Linux")

    @mock.patch("sys.platform", "darwin")
    def test_get_platform_darwin(self):
        platform = get_platform()
        self.assertTrue(platform == "Mac")

    @mock.patch("sys.platform", "win32")
    def test_get_platform_win32(self):
        platform = get_platform()
        self.assertTrue(platform == "Windows")

    @mock.patch("sys.platform", "win32")
    @mock.patch.dict("os.environ", {"MSYSTEM": "MINGW64"})
    def test_get_platform_win32git(self):
        platform = get_platform()
        self.assertTrue(platform == "WindowsGitBash")
