import pytest
from Pages.SignupPage import SignUpPage
from playwright.sync_api import Page, expect


def test_page(page: Page):
    signup_page = SignUpPage(page)
    expect(page).to_have_url("https://automationexercise.com/login")
    expect(page.get_by_text("New User Signup!")).to_be_visible()

def test_signup(page: Page, random_user: dict):

    signup_page = SignUpPage(page)
    signup_page.signup(username = random_user["username"], email = random_user["email"])

    expect(page.get_by_text("ENTER ACCOUNT INFORMATION")).to_be_visible()

def test_already_existing_user(page: Page):
    signup_page = SignUpPage(page)
    signup_page.signup(username = "test", email = "test@test.com")

    expect(page.get_by_text("Email Address already exist!")).to_be_visible()

def test_empty_name_and_email_signup(page: Page):
    signup_page = SignUpPage(page)
    signup_page.signup(username = "", email = "")

    email_input = page.get_by_placeholder("Email Address").nth(1)
    is_invalid = email_input.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_only_empty_email_signup(page: Page):
    signup_page = SignUpPage(page)
    signup_page.signup(username = "asdasd", email = "")

    email_input = page.get_by_placeholder("Email Address").nth(1)
    is_invalid = email_input.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_invalid_email_format(page: Page, random_user: dict):
    signup_page = SignUpPage(page)
    signup_page.signup(username = random_user["username"], email = random_user["email"].replace("@", ""))

    email_input = page.get_by_placeholder("Email Address").nth(1)
    is_invalid = email_input.evaluate("el => el.validity.typeMismatch")
    assert is_invalid
