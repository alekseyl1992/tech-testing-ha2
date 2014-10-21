import os
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions

from selenium.webdriver.support.wait import WebDriverWait
import time

from tests.objects.abstract import Form, Page, Component, Polling


class CreatePage(Page):
    PATH = '/ads/create'

    def __init__(self, driver):
        super(CreatePage, self).__init__(driver)

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


class OrganizationCreateForm(Form):
    PRODUCT_TYPE = '#product-type-6039'
    BASE_TYPE = '#pad-mobile_app_mobile_service'
    COMPANY_INPUT = '.base-setting__campaign-name__input'

    COMPANY_NAME = 'My Test Company'

    def __init__(self, driver):
        super(OrganizationCreateForm, self).__init__(driver)
        pass

    def wait(self):
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
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
    IMAGE_PREVIEW = '.banner-preview__img'
    MARKET_INPUT = 'div.banner-form__body > ul > li:nth-child(4) > span.banner-form__input-wrapper > input'
    SUBMIT = '.main-button__label'

    RESTRICTION_LINE = '//*[@data-node-id=\'restrict\']'
    RESTRICTION_RADIO = '//*[@id=\'restrict-%s\']'
    RESTRICTION_LABEL = '//*[@for=\'restrict-%s\']'

    WORK_TIME_LINE = '//div[@data-name=\'date\']/*[contains(@class, \'campaign-setting__value\')]'
    WORK_TIME_DATE_FROM = '//input[@data-name=\'from\']'
    WORK_TIME_DATE_TO = '//input[@data-name=\'to\']'

    IMAGE_FILE = '../../img/logo.png'
    MARKET_LINK = 'https://play.google.com/store/apps/details?id=com.maxmpz.audioplayer'

    def __init__(self, driver):
        super(AdCreateForm, self).__init__(driver)

    def wait(self):
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_css_selector(self.MARKET_INPUT)
        )

    def set_restriction(self, restriction):
        self.driver.find_element_by_xpath(self.RESTRICTION_LINE).click()

        el = WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_xpath(self.RESTRICTION_RADIO % restriction)
        )
        el.click()

        label = WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_xpath(self.RESTRICTION_LABEL % restriction)
        )
        return label.text

    def get_restriction_line_text(self):
        el = self.driver.find_element_by_xpath(self.RESTRICTION_LINE)
        return el.text

    def is_restriction_selected(self, restriction):
        el = self.driver.find_element_by_xpath(self.RESTRICTION_RADIO % restriction)
        return el.get_attribute('checked')

    def get_work_time_line_text(self):
        text = self.driver.find_element_by_xpath(self.WORK_TIME_LINE).text
        return text

    def set_work_time_by_input(self, from_time, to_time):
        line_el = self.driver.find_element_by_xpath(self.WORK_TIME_LINE)
        from_el = self.driver.find_element_by_xpath(self.WORK_TIME_DATE_FROM)
        to_el = self.driver.find_element_by_xpath(self.WORK_TIME_DATE_TO)

        # uncollapse and wait for visibility
        def uncollapse(driver):
            try:
                line_el.click()
                return True
            except WebDriverException:
                return False

        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD)\
            .until(uncollapse)

        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD)\
            .until(expected_conditions
                   .visibility_of(from_el))

        from_el.send_keys(from_time)
        to_el.send_keys(to_time)

        # unfocus inputs
        line_el.click()

    def set_work_time_by_date_picker(self, from_time, to_time):
        pass

    def set_image(self, file_name):
        element = WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_css_selector(self.IMAGE_INPUT)
        )

        file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + file_name
        element.send_keys(file_path)

        # wait for it to be loaded
        preview_el = self.driver.find_element_by_css_selector(self.IMAGE_PREVIEW)

        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: preview_el.value_of_css_property('display') == 'block'
        )

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

