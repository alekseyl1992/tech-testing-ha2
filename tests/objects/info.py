from tests.objects.abstract import Page
from tests.objects.edit import AdEditPage


class InfoPage(Page):
    def __init__(self, driver):
        super(InfoPage, self).__init__(driver)

    def edit_page(self):
        return AdEditPage(self.driver)