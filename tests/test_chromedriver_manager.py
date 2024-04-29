

import unittest
import os
from unittest.mock import MagicMock, patch
from chromeDriverManager.chromedriver_manager import ChromeDriverManager


class TestChromeDriverManager(unittest.TestCase):
    def setUp(self):
        self.driver = ChromeDriverManager().install()
        print(self.driver)

    def test_install(self):
        self.assertTrue(os.path.exists(self.driver))
