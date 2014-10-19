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

    def test(self):
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
        create_page.ad_form.set_fields(age=[10, 20],
                                       work_time=['29.10.2014', '31.10.2014'])
        
        info_page = create_page.ad_form.submit()


        edit_page = info_page.edit_page()

        # asserts here

        email = create_page.top_menu.get_email()

        # time.sleep(5)

        self.assertEqual(USERNAME, email)

        # ## And some examples
        # create_page.slider.move(100)
        # FILE_PATH = '/Users/bayandin/repos/tech-testing-selenium-demo/img.jpg'
        # element = WebDriverWait(self.driver, 30, 0.1).until(
        #     lambda d: d.find_element_by_css_selector('.banner-form__img-file')
        # )
        #
        # element.send_keys(FILE_PATH)

        # os.path.dirname(os.path.abspath(__file__)) // path to script
        # os.getcwd() // cwd
        # + 'logo.png'

        market_link = 'https://play.google.com/store/apps/details?id=com.maxmpz.audioplayer'