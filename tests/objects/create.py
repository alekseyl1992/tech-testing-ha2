from selenium.webdriver.support.wait import WebDriverWait
from tests.objects.abstract import Form, Page, Component
from tests.objects.info import InfoPage


class CreatePage(Page):
    PATH = '/ads/create'

    def __init__(self, driver):
        super(CreatePage, self).__init__(driver)

        self.top_menu = TopMenu(self.driver)
        self.organization_form = OrganizationCreateForm(driver)
        self.ad_form = AdCreateForm(driver)


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


class OrganizationCreateForm(Form):
    def __init__(self, driver):
        super(OrganizationCreateForm, self).__init__(driver)
        pass

    def submit(self):
        pass


class EditPage(Page):
    def __init__(self, driver):
        super(EditPage, self).__init__(driver)
        pass


class AdCreateForm(Form):
    def __init__(self, driver):
        super(AdCreateForm, self).__init__(driver)

        self.slider = Slider(self.driver)

    def set_fields(self, age, work_time):
        pass

    def submit(self):
        return InfoPage(self.driver)