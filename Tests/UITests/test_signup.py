import pytest
from Pages.SignupPage import SignUpPage
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_signup_page_loads(signup_page):
    expect(signup_page.page).to_have_url("https://automationexercise.com/login")
    expect(signup_page.page.get_by_text("New User Signup!")).to_be_visible()

@pytest.mark.smoke
def test_signup(signup_page, random_user: dict):
    signup_page.signup(username = random_user["username"], email = random_user["email"])

    expect(signup_page.page.get_by_text("ENTER ACCOUNT INFORMATION")).to_be_visible()

@pytest.mark.regression
def test_already_existing_user(signup_page):
    signup_page.signup(username = "test", email = "test@test.com")

    expect(signup_page.page.get_by_text("Email Address already exist!")).to_be_visible()

@pytest.mark.regression
def test_empty_name_and_email_signup(signup_page):
    signup_page.signup(username = "", email = "")

    is_invalid = signup_page.signup_username_input.evaluate("el => !el.validity.valid")
    assert is_invalid

@pytest.mark.regression
def test_only_empty_email_signup(signup_page):
    signup_page.signup(username = "asdasd", email = "")

    is_invalid = signup_page.signup_email_input.evaluate("el => !el.validity.valid")
    assert is_invalid

@pytest.mark.regression
def test_invalid_email_format(signup_page, random_user: dict):
    signup_page.signup(username = random_user["username"], email = random_user["email"].replace("@", ""))

    is_invalid = signup_page.signup_email_input.evaluate("el => el.validity.typeMismatch")
    assert is_invalid
