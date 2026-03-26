import pytest
import uuid
from Pages.ContactUsPage import ContactUsPage
from Pages.LoginPage import LoginPage
from playwright.sync_api import Page
from Pages.RegisterPage import RegisterPage
from Pages.SignupPage import SignUpPage
from Pages.BasePage import BasePage


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

@pytest.fixture
def register_page(page: Page, signup_page, register_user):
    signup_page.signup(username=register_user["username"], email=register_user["email"])
    return RegisterPage(page)

@pytest.fixture
def test_cases_page(page: Page):
    base_page = BasePage(page)
    base_page.navigate("/test_cases")
    return base_page

@pytest.fixture
def random_user():
    return {
        "username": "user_" + uuid.uuid4().hex[:6],
        "email": f"{uuid.uuid4().hex[:8]}@test.com",
    }

