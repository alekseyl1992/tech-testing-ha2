import os
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select

from selenium.webdriver.support.wait import WebDriverWait
import time
from tests import common

from tests.objects.abstract import Form, Page, Component
from tests.common import Polling


class CreatePage(Page):
    PATH = '/ads/create'

    def __init__(self, driver):
        super(CreatePage, self).__init__(driver)

        self.organization_form = OrganizationCreateForm(self.driver)
        self.ad_form = AdCreateForm(self.driver)

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

    def configure(self):
        el = common.wait_and_get_by_css(self.driver, self.COMPANY_INPUT)
        el.clear()
        el.send_keys(self.COMPANY_NAME)

        common.wait_and_get_by_css(self.driver, self.PRODUCT_TYPE).click()
        common.wait_and_get_by_css(self.driver, self.BASE_TYPE).click()

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

    DATE_PICKER_MONTH = '.ui-datepicker-month'
    DATE_PICKER_YEAR = '.ui-datepicker-year'
    DATE_PICKER_DAY = '//*[@class=\'ui-datepicker-calendar\']//td/a[text()=%s]'

    IMAGE_FILE = '../../img/logo_new.png'
    MARKET_LINK = 'https://play.google.com/store/apps/details?id=com.maxmpz.audioplayer'

    def __init__(self, driver):
        super(AdCreateForm, self).__init__(driver)

    def wait(self):
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_css_selector(self.MARKET_INPUT)
        )

    def set_restriction(self, restriction):
        restriction_line = common.wait_and_get_by_xpath(self.driver, self.RESTRICTION_LINE)
        self.uncollapse_element(restriction_line)

        el = WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_xpath(self.RESTRICTION_RADIO % restriction)
        )
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD)\
            .until(expected_conditions
                   .visibility_of(el))

        el.click()

        label = WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_xpath(self.RESTRICTION_LABEL % restriction)
        )
        return label.text

    def get_restriction_line_text(self):
        el = common.wait_and_get_by_xpath(self.driver, self.RESTRICTION_LINE)
        return el.text

    def is_restriction_selected(self, restriction):
        el = common.wait_and_get_by_xpath(self.driver, self.RESTRICTION_RADIO % restriction)
        return el.get_attribute('checked')

    def get_work_time_line_text(self):
        text = common.wait_and_get_by_xpath(self.driver, self.WORK_TIME_LINE).text
        return text

    def uncollapse_element(self, element):
        def uncollapse(driver):
            try:
                element.click()
                return True
            except WebDriverException:
                return False

        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD)\
            .until(uncollapse)

    def set_work_time_by_input(self, from_time, to_time):
        line_el = common.wait_and_get_by_xpath(self.driver, self.WORK_TIME_LINE)
        self.uncollapse_element(line_el)

        from_el = common.wait_and_get_by_xpath(self.driver, self.WORK_TIME_DATE_FROM)
        to_el = common.wait_and_get_by_xpath(self.driver, self.WORK_TIME_DATE_TO)

        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD)\
            .until(expected_conditions
                   .visibility_of(from_el))

        from_el.send_keys(from_time)
        to_el.send_keys(to_time)

        # unfocus inputs
        line_el.click()

    def get_date_picker(self, xpath):
        line_el = common.wait_and_get_by_xpath(self.driver, self.WORK_TIME_LINE)
        self.uncollapse_element(line_el)

        input_el = common.wait_and_get_by_xpath(self.driver, xpath)
        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD)\
            .until(expected_conditions
                   .visibility_of(input_el))

        input_el.click()  # show date picker

        return DatePicker(self.driver)

    def set_work_time_by_date_picker(self, xpath, month, year, day):
        date_picker = self.get_date_picker(xpath)

        date_picker_month = common.wait_and_get_by_css(self.driver, self.DATE_PICKER_MONTH)
        Select(date_picker_month).select_by_value(month)

        date_picker_year = common.wait_and_get_by_css(self.driver, self.DATE_PICKER_YEAR)
        Select(date_picker_year).select_by_value(year)

        day_picker_day = common.wait_and_get_by_xpath(self.driver, self.DATE_PICKER_DAY % day)
        day_picker_day.click()

        # collapse to default state
        line_el = common.wait_and_get_by_xpath(self.driver, self.WORK_TIME_LINE)
        line_el.click()

    def set_image(self, file_name):
        element = WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: d.find_element_by_css_selector(self.IMAGE_INPUT)
        )

        file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + file_name
        element.send_keys(file_path)

        # wait for it to be loaded
        preview_el = common.wait_and_get_by_css(self.driver, self.IMAGE_PREVIEW)

        WebDriverWait(self.driver, Polling.TIMEOUT, Polling.PERIOD).until(
            lambda d: preview_el.value_of_css_property('display') == 'block'
        )

    def set_market_link(self, market_link):
        common.wait_and_get_by_css(self.driver, self.MARKET_INPUT).send_keys(market_link)
        pass

    def configure(self):
        self.set_market_link(self.MARKET_LINK)
        self.set_image(self.IMAGE_FILE)

    def submit(self):
        common.wait_and_get_by_css(self.driver, self.SUBMIT).click()

        from tests.objects.info import InfoPage
        return InfoPage(self.driver)


class DatePicker(Component):
    MONTH_SELECT = '.ui-datepicker-month'

    PREV_ARROW = '.ui-datepicker-prev'
    NEXT_ARROW = '.ui-datepicker-next'

    def press_prev_arrow(self):
        common.wait_and_get_by_css(self.driver, self.PREV_ARROW).click()

    def press_next_arrow(self):
        common.wait_and_get_by_css(self.driver, self.NEXT_ARROW).click()

    def get_month(self):
        return Select(self.driver
                      .find_element_by_css_selector(self.MONTH_SELECT))\
            .first_selected_option.get_attribute('value')