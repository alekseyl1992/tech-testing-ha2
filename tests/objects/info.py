from selenium.webdriver.support.wait import WebDriverWait
from tests import common
from tests.objects.abstract import Page
from tests.common import Polling
from tests.objects.edit import AdEditPage


class InfoPage(Page):
    PATH = '/ads/campaigns/'

    EDIT_LINK = '.control__link_edit'
    DELETE_LINK = '.control__preset_delete'

    def __init__(self, driver):
        super(InfoPage, self).__init__(driver)

    def edit_page(self):
        common.wait_and_get_by_css(self.driver, self.EDIT_LINK).click()
        return AdEditPage(self.driver)

    def delete(self):
        self.driver.get(self.BASE_URL + self.PATH)  # ensure we are at campaign list
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_css_selector(self.DELETE_LINK)
        ).click()