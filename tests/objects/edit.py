from selenium.webdriver.support.wait import WebDriverWait
from tests.objects.create import CreatePage, AdCreateForm


class AdEditPage(CreatePage):
    def __init__(self, driver):
        super(AdEditPage, self).__init__(driver)

    def wait(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.organization_form.COMPANY_INPUT)
        )

        return self


class AdEditForm(AdCreateForm):
    def __init__(self, driver):
        super(AdEditForm, self).__init__(driver)