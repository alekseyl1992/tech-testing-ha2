import os

from selenium.webdriver.support.wait import WebDriverWait
from tests.objects.abstract import Form, Page, Component


class CreatePage(Page):
    PATH = '/ads/create'

    def __init__(self, driver):
        super(CreatePage, self).__init__(driver)

        self.top_menu = TopMenu(self.driver)
        self.organization_form = OrganizationCreateForm(self.driver)
        self.ad_form = AdCreateForm(self.driver)

    def wait(self):
        self.organization_form.wait()
        self.ad_form.wait()
        return self

    def configure(self):
        self.organization_form.configure()
        self.ad_form.configure()
        return self


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
    PRODUCT_TYPE = '#product-type-6039'
    BASE_TYPE = '#pad-mobile_app_mobile_service'
    COMPANY_INPUT = '.base-setting__campaign-name__input'

    COMPANY_NAME = 'My Test Company'

    def __init__(self, driver):
        super(OrganizationCreateForm, self).__init__(driver)
        pass

    def wait(self):
        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.COMPANY_INPUT)
        )

    def configure(self):
        el = self.driver.find_element_by_css_selector(self.COMPANY_INPUT)
        el.clear()
        el.send_keys(self.COMPANY_NAME)

        self.driver.find_element_by_css_selector(self.PRODUCT_TYPE).click()
        self.driver.find_element_by_css_selector(self.BASE_TYPE).click()

    def submit(self):
        pass


class AdCreateForm(Form):
    IMAGE_INPUT = '.banner-form__img-file'
    MARKET_INPUT = 'div.banner-form__body > ul > li:nth-child(4) > span.banner-form__input-wrapper > input'
    SUBMIT = '.main-button__label'

    RESTRICTION_LINE = '//*[@data-node-id=\'restrict\']'

    RESTRICTION_RADIO = '//*[@id=\'restrict-%s\']'
    RESTRICTION_LABEL = '//*[@for=\'restrict-%s\']'

    IMAGE_FILE = '../../img/logo.png'
    MARKET_LINK = 'https://play.google.com/store/apps/details?id=com.maxmpz.audioplayer'

    def __init__(self, driver):
        super(AdCreateForm, self).__init__(driver)

        self.slider = Slider(self.driver)

    def wait(self):
        # WebDriverWait(self.driver, 30, 0.1)\
        #     .until(expected_conditions
        #            .visibility_of(self.driver
        #                           .find_element_by_css_selector(self.MARKET_INPUT)))

        WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.MARKET_INPUT)
        )

    def set_restriction(self, restriction):
        self.driver.find_element_by_xpath(self.RESTRICTION_LINE).click()

        el = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.RESTRICTION_RADIO % restriction)
        )
        el.click()

        label = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.RESTRICTION_LABEL % restriction)
        )
        return label.text

    def get_restriction_line_text(self):
        el = self.driver.find_element_by_xpath(self.RESTRICTION_LINE)
        return el.text

    def is_restriction_selected(self, restriction):
        el = self.driver.find_element_by_xpath(self.RESTRICTION_RADIO % restriction)
        return el.get_attribute('checked')

    def set_work_time(self, from_time, to_time):
        pass

    def set_image(self, file_name):
        element = WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_css_selector(self.IMAGE_INPUT)
        )

        file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + file_name
        element.send_keys(file_path)

    def set_market_link(self, market_link):
        self.driver.find_element_by_css_selector(self.MARKET_INPUT).send_keys(market_link)
        pass

    def configure(self):
        self.set_market_link(self.MARKET_LINK)
        self.set_image(self.IMAGE_FILE)

    def submit(self):
        self.driver.find_element_by_css_selector(self.SUBMIT).click()

        from tests.objects.info import InfoPage
        return InfoPage(self.driver).wait()

