import pytest
from playwright.sync_api import Page, expect
from Pages.LoginPage import LoginPage


def test_page(page: Page):
    login_page = LoginPage(page)
    expect(page).to_have_url("https://automationexercise.com/login")
    expect(page.get_by_text("Login to your account")).to_be_visible()

def test_valid_user_login(page: Page, existing_user: dict):
    login_page = LoginPage(page)
    login_page.login(email = existing_user["email"], password = existing_user["password"])

    expect(page).to_have_url("https://automationexercise.com/")
    expect(page.get_by_text("Logout")).to_be_visible()
    expect(page.get_by_text("Delete Account")).to_be_visible()
    expect(page.get_by_text(f"Logged in as {existing_user['username']}")).to_be_visible()

@pytest.mark.parametrize("users", [
    pytest.param({
        "username": "JohnDoe123",
        "email": "testuser_JohnDoe@test.com",
        "password": "John123",
    }, id = "email+pass_incorrect"),
    pytest.param({
        "username": "JaneSmith123",
        "email": "KvatiTest@test.com",
        "password": "Jane123",
    },id = "only_pass_incorrect")
])
def test_invalid_user_login(page: Page, users: dict):
    login_page = LoginPage(page)
    login_page.login(email = users["email"], password = users["password"])

    expect(page.get_by_text("Your email or password is incorrect!")).to_be_visible()

def test_empty_values_login(page: Page):
    login_page = LoginPage(page)
    login_page.login(email = "", password = "")

    email_input = page.get_by_placeholder("Email Address").nth(0)
    is_invalid = email_input.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_empty_password_login(page: Page):
    login_page = LoginPage(page)
    login_page.login(email = "test@test.com", password = "")

    password_input = page.get_by_placeholder("Password")
    is_invalid = password_input.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_logout(page: Page, existing_user: dict):
    login_page = LoginPage(page)
    login_page.login(email=existing_user["email"], password=existing_user["password"])

    expect(page.get_by_text(f"Logged in as {existing_user['username']}")).to_be_visible()

    login_page.logout()
    expect(page).to_have_url("https://automationexercise.com/login")
    expect(page.get_by_text("Login to your account")).to_be_visible()