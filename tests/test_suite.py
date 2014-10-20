import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote

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

    def test_age(self):
        create_page = self.get_create_page().wait()
        create_page.organization_form.configure()
        create_page.ad_form.configure()

        expected_age_min = 18
        expected_age_max = 30

        create_page.ad_form.set_age(expected_age_min,
                                    expected_age_max)
        
        info_page = create_page.ad_form.submit()
        edit_page = info_page.edit_page()

        time.sleep(10)

        # asserts here

        # email = create_page.top_menu.get_email()

        # time.sleep(5)

        # self.assertEqual(USERNAME, email)