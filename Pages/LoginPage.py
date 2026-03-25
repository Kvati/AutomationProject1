from playwright.sync_api import Page
from BasePage import BasePage

class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.navigate("https://automationexercise.com/login")

        self.login_username_input = page.get_by_placeholder("Email Address")
        self.login_password_input = page.get_by_placeholder("Password")

        self.login_button = page.get_by_role("button", name = "Login")


    def login(self, email: str, password: str):

        self.login_username_input.fill(email)
        self.login_password_input.fill(password)

        self.login_button.click()


