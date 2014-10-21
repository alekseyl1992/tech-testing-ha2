import urlparse


class Page(object):
    BASE_URL = 'https://target.mail.ru'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class Form(Component):
    def __init__(self, driver):
        super(Form, self).__init__(driver)
        pass

    def configure(self):
        raise NotImplementedError()

    def submit(self):
        raise NotImplementedError()
