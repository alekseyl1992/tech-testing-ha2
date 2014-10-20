from selenium.webdriver.support.wait import WebDriverWait
from tests.objects.abstract import Page
from tests.objects.edit import AdEditPage


class InfoPage(Page):
    EDIT_LINK = '.control__link control__link_edit'

    def __init__(self, driver):
        super(InfoPage, self).__init__(driver)

    def wait(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.EDIT_LINK)
        )

        return self

    def edit_page(self):
        self.driver.find_element_by_css_selector(self.EDIT_LINK).click()
        return AdEditPage(self.driver).wait()