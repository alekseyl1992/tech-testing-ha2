from tests.objects.abstract import Page, Form


class AdEditPage(Page):
    def __init__(self, driver):
        super(AdEditPage, self).__init__(driver)


class AdEditForm(Form):
    def __init__(self, driver):
        super(AdEditForm, self).__init__(driver)