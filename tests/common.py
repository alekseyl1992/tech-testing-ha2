import os
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_BROWSER = 'CHROME'
GRID_URL = 'http://127.0.0.1:4444/wd/hub'


class Polling:
    def __init__(self):
        pass

    TIMEOUT = 30
    PERIOD = 0.1


def wait_and_get_by_css(driver, selector):
    return WebDriverWait(driver, Polling.TIMEOUT, Polling.PERIOD).until(
        lambda d: d.find_element_by_css_selector(selector)
    )


def wait_and_get_by_xpath(driver, selector):
    return WebDriverWait(driver, Polling.TIMEOUT, Polling.PERIOD).until(
        lambda d: d.find_element_by_xpath(selector)
    )

def get_create_page(driver):
    USERNAME = 'tech-testing-ha2-17@bk.ru'
    PASSWORD = os.environ['TTHA2PASSWORD']
    DOMAIN = '@bk.ru'

    import tests.objects.auth as auth
    auth_page = auth.AuthPage(driver)
    auth_page.open()

    auth_form = auth_page.form
    auth_form.set_domain(DOMAIN)
    auth_form.set_login(USERNAME)
    auth_form.set_password(PASSWORD)
    auth_form.submit()

    import tests.objects.create as create
    create_page = create.CreatePage(driver)
    create_page.open()

    return create_page