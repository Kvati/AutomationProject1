from Pages.BasePage import BasePage
from playwright.sync_api import Page


class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.navigate("https://automationexercise.com/")

