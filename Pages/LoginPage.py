from playwright.sync_api import Page
from Pages.BasePage import BasePage

class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.logout_button = page.get_by_text("Logout")

        self.login_email_input = page.get_by_placeholder("Email Address").nth(0)
        self.login_password_input = page.get_by_placeholder("Password")

        self.login_button = page.get_by_role("button", name = "Login")

    def navigate_to_login_page(self):
        self.navigate("https://automationexercise.com/login")

    def login(self, email: str, password: str):

        self.login_email_input.fill(email)
        self.login_password_input.fill(password)

        self.login_button.click()

    def logout(self):
        self.logout_button.click()

