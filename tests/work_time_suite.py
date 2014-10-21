import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote
import time
from tests import common

from tests.objects.auth import AuthPage
from tests.objects.create import CreatePage


class WorkTimeSuite(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', common.DEFAULT_BROWSER)

        self.driver = Remote(
            command_executor=common.GRID_URL,
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        self.create_page = common.get_create_page(self.driver).wait().configure()

    def tearDown(self):
        self.driver.quit()


