from selenium.webdriver.support.wait import WebDriverWait
from tests.objects.abstract import Page, Polling
from tests.objects.edit import AdEditPage


class InfoPage(Page):
    PATH = '/ads/campaigns/'

    EDIT_LINK = '.control__link_edit'
    DELETE_LINK = '.control__preset_delete'

    def __init__(self, driver):
        super(InfoPage, self).__init__(driver)

    def wait(self):
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_css_selector(self.EDIT_LINK)
        )

        return self

    def edit_page(self):
        self.driver.find_element_by_css_selector(self.EDIT_LINK).click()
        return AdEditPage(self.driver).wait()

    def delete(self):
        self.driver.get(self.BASE_URL + self.PATH)  # ensure we are at campaign list
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_css_selector(self.DELETE_LINK)
        ).click()