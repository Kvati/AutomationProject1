import pytest

from Pages.ContactUsPage import ContactUsPage
from Pages.LoginPage import LoginPage
from playwright.sync_api import Page
from Pages.SignupPage import SignUpPage


@pytest.fixture
def login_page(page: Page):
    login_page = LoginPage(page)
    login_page.navigate_to_login_page()
    return login_page

@pytest.fixture
def signup_page(page: Page):
    signup_page = SignUpPage(page)
    signup_page.navigate_to_signup_page()
    return signup_page

@pytest.fixture
def contact_page(page: Page):
    contact_us_page = ContactUsPage(page)
    contact_us_page.navigate_to_contactus_page()
    return contact_us_page