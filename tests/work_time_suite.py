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
        """
        Tests work time line visual changes (without sending)
        (using keyboard input)
        """

        from_time = '20.10.2014'
        to_time = '25.10.2014'
        days_count = 6

        self.create_page.ad_form.set_work_time_by_input(from_time, to_time)

        text = self.create_page.ad_form.get_work_time_line_text()
        actual_days_count = int(text.split()[0])

        self.assertEquals(days_count, actual_days_count)

    def test_work_time_line_changes_by_date_picker(self):
        """
        Tests work time line visual changes (without sending)
        (using date picker)
        """

        month_from = '11'
        year_from = '2014'
        day_from = '01'

        month_to = '11'
        year_to = '2014'
        day_to = '31'

        days_count = 31

        self.create_page.ad_form\
            .set_work_time_by_date_picker(self.create_page.ad_form.WORK_TIME_DATE_FROM,
                                          month_from,
                                          year_from,
                                          day_from)

        self.create_page.ad_form\
            .set_work_time_by_date_picker(self.create_page.ad_form.WORK_TIME_DATE_TO,
                                          month_to,
                                          year_to,
                                          day_to)

        text = self.create_page.ad_form.get_work_time_line_text()
        actual_days_count = int(text.split()[0])

        self.assertEquals(days_count, actual_days_count)

    def test_work_time_saved(self):
        """
        Tests work time in edit page
        """

        self.create_page.configure()

        from_time = '20.10.2014'
        to_time = '25.10.2014'
        days_count = 6

        self.create_page.ad_form.set_work_time_by_input(from_time, to_time)

        info_page = self.create_page.ad_form.submit()
        edit_page = info_page.edit_page()

        text = edit_page.ad_form.get_work_time_line_text()
        actual_days_count = int(text.split()[0])

        info_page.delete()

        self.assertEquals(days_count, actual_days_count)

    def test_date_picker_arrows(self):
        """
        Tests left and right arrows, that should change months
        """

        xpath = self.create_page.ad_form.WORK_TIME_DATE_FROM

        date_picker = self.create_page.ad_form.get_date_picker(xpath)
        month_before = date_picker.get_month()

        date_picker.press_next_arrow()
        month_next = date_picker.get_month()

        date_picker.press_prev_arrow()
        month_next_prev = date_picker.get_month()

        self.assertEquals(month_before, month_next_prev)

        self.assertTrue((int(month_before) + 1) % 12 == int(month_next))