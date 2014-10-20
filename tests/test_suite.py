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


    # def test_restriction_none(self):
    #     create_page = self.get_create_page().wait().configure()
    #
    #     expected_restriction = create_page.ad_form.RESTRICTION_NONE
    #     expected_restriction_text = create_page.ad_form.set_restriction(expected_restriction)
    #
    #     info_page = create_page.ad_form.submit()
    #     edit_page = info_page.edit_page()
    #
    #     actual_restriction = edit_page.get_restriction_id()
    #     actual_restriction_text = edit_page.get_restriction_text()
    #
    #     self.assertEquals(expected_restriction, actual_restriction)
    #     self.assertEquals(expected_restriction_text, actual_restriction_text)