from selenium.webdriver.support.select import Select
from tests import common
from tests.objects.abstract import Page, Component


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class AuthForm(Component):
    LOGIN = '#id_Login'
    PASSWORD = '#id_Password'
    DOMAIN = '#id_Domain'
    SUBMIT = '#gogogo>input'

    def set_login(self, login):
        common.wait_and_get_by_css(self.driver, self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        common.wait_and_get_by_css(self.driver, self.PASSWORD).send_keys(pwd)

    def set_domain(self, domain):
        select = common.wait_and_get_by_css(self.driver, self.DOMAIN)
        Select(select).select_by_visible_text(domain)

    def submit(self):
        common.wait_and_get_by_css(self.driver, self.SUBMIT).click()