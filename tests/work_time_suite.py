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

        self.create_page = common.get_create_page(self.driver).wait()

    def tearDown(self):
        self.driver.quit()

    def test_work_time_line_changes_by_input(self):
        from_time = '20.10.2014'
        to_time = '25.10.2014'
        days_count = 6

        self.create_page.ad_form.set_work_time_by_input(from_time, to_time)

        text = self.create_page.ad_form.get_work_time_line_text()
        actual_days_count = int(text.split()[0])

        self.assertEquals(days_count, actual_days_count)

    # def test_work_time_line_changes_by_date_picker(self):
    #     pass
    #
    # def test_work_time_saved(self):
    #     pass