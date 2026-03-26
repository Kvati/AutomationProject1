from playwright.sync_api import Page
from Pages.BasePage import BasePage

class SignUpPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.signup_username_input = page.get_by_placeholder("Name")
        self.signup_email_input = page.get_by_placeholder("Email Address").nth(1)

        self.signup_button = page.get_by_role("button", name="Signup")

    def navigate_to_signup_page(self):
        self.navigate("https://automationexercise.com/login")


    def signup(self, username: str, email: str):

        self.signup_username_input.fill(username)
        self.signup_email_input.fill(email)

        self.signup_button.click()
