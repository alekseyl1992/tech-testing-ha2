import os
import unittest
import common
from selenium.webdriver import DesiredCapabilities, Remote


class RestrictionSuite(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', common.DEFAULT_BROWSER)

        self.driver = Remote(
            command_executor=common.GRID_URL,
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        self.create_page = common.get_create_page(self.driver).wait()

    def tearDown(self):
        self.driver.quit()

    def test_restriction_line_changes(self):
        """
        Tests visual changes without creating of campaign
        """

        expected_restriction = '18+'
        expected_restriction_text = self.create_page.ad_form.set_restriction(expected_restriction)

        restriction_line_text = self.create_page.ad_form.get_restriction_line_text()

        self.assertEquals(expected_restriction_text, restriction_line_text)

    def _test_restriction_saved(self, restriction):
        """
        Compares selected restriction on create page with those on edit page
        :param restriction: one of ('', '12+', '14+', '16+ '18+')
        """
        self.create_page.configure()

        expected_restriction_text = self.create_page.ad_form.set_restriction(restriction)

        info_page = self.create_page.ad_form.submit()
        edit_page = info_page.edit_page()

        actual_restriction_text = edit_page.ad_form.get_restriction_line_text()

        self.assertTrue(edit_page.ad_form.is_restriction_selected(restriction))
        self.assertEquals(expected_restriction_text, actual_restriction_text)

    def test_restriction_none_saved(self):
        """
        Tests for Not specified restriction
        """
        self._test_restriction_saved('')

    def test_restriction_16_saved(self):
        """
        Tests for 16+ restriction
        """
        self._test_restriction_saved('16+')
