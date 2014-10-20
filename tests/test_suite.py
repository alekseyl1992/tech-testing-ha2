import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote
import time

from tests.objects.auth import AuthPage
from tests.objects.create import CreatePage


class TestSuite(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def get_create_page(self):
        USERNAME = 'tech-testing-ha2-17@bk.ru'
        PASSWORD = os.environ['TTHA2PASSWORD']
        DOMAIN = '@bk.ru'

        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.set_domain(DOMAIN)
        auth_form.set_login(USERNAME)
        auth_form.set_password(PASSWORD)
        auth_form.submit()

        create_page = CreatePage(self.driver)
        create_page.open()

        return create_page

    def test_restriction_line_changes(self):
        create_page = self.get_create_page().wait().configure()

        expected_restriction = '18+'
        expected_restriction_text = create_page.ad_form.set_restriction(expected_restriction)

        restriction_line_text = create_page.ad_form.get_restriction_line_text()

        self.assertEquals(expected_restriction_text, restriction_line_text)

    def _test_restriction_on_edit_page(self, restriction):
        create_page = self.get_create_page().wait().configure()

        expected_restriction_text = create_page.ad_form.set_restriction(restriction)

        #time.sleep(5)

        info_page = create_page.ad_form.submit()
        edit_page = info_page.edit_page()

        actual_restriction_text = edit_page.ad_form.get_restriction_line_text()

        self.assertTrue(edit_page.ad_form.is_restriction_selected(restriction))
        self.assertEquals(expected_restriction_text, actual_restriction_text)

    def test_restriction_none_on_edit_page(self):
        self._test_restriction_on_edit_page('')

    def test_restriction_16_on_edit_page(self):
        self._test_restriction_on_edit_page('16+')