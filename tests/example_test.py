import os

import unittest
import urlparse

from selenium.webdriver import ActionChains, DesiredCapabilities, Remote
from selenium.webdriver.support.ui import Select, WebDriverWait


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class CreatePage(Page):
    PATH = '/ads/create'

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def slider(self):
        return Slider(self.driver)


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '#id_Login'
    PASSWORD = '#id_Password'
    DOMAIN = '#id_Domain'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        self.driver.find_element_by_css_selector(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_css_selector(self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = self.driver.find_element_by_css_selector(self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()


class TopMenu(Component):
    EMAIL = '#PH_user-email'

    def get_email(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EMAIL).text
        )


class Slider(Component):
    SLIDER = '.price-slider__begunok'

    def move(self, offset):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.SLIDER)
        )
        ac = ActionChains(self.driver)
        ac.click_and_hold(element).move_by_offset(offset, 0).perform()


class ExampleTest(unittest.TestCase):
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
        email = create_page.top_menu.get_email()

        self.assertEqual(USERNAME, email)

        # ## And some examples
        # create_page.slider.move(100)
        # FILE_PATH = '/Users/bayandin/repos/tech-testing-selenium-demo/img.jpg'
        # element = WebDriverWait(self.driver, 30, 0.1).until(
        #     lambda d: d.find_element_by_css_selector('.banner-form__img-file')
        # )
        #
        # element.send_keys(FILE_PATH)
