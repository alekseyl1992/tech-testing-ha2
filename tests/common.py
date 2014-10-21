import os
from tests.objects.auth import AuthPage
from tests.objects.create import CreatePage

DEFAULT_BROWSER = 'CHROME'
GRID_URL = 'http://127.0.0.1:4444/wd/hub'

def get_create_page(driver):
    USERNAME = 'tech-testing-ha2-17@bk.ru'
    PASSWORD = os.environ['TTHA2PASSWORD']
    DOMAIN = '@bk.ru'

    auth_page = AuthPage(driver)
    auth_page.open()

    auth_form = auth_page.form
    auth_form.set_domain(DOMAIN)
    auth_form.set_login(USERNAME)
    auth_form.set_password(PASSWORD)
    auth_form.submit()

    create_page = CreatePage(driver)
    create_page.open()

    return create_page