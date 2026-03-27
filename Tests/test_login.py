import pytest
from playwright.sync_api import expect


def test_page(login_page):

    expect(login_page.page).to_have_url("https://automationexercise.com/login")
    expect(login_page.page.get_by_text("Login to your account")).to_be_visible()

def test_valid_user_login(login_page, existing_user: dict):
    login_page.login(email = existing_user["email"], password = existing_user["password"])

    expect(login_page.page).to_have_url("https://automationexercise.com/")
    expect(login_page.page.get_by_text("Logout")).to_be_visible()
    expect(login_page.page.get_by_text("Delete Account")).to_be_visible()
    expect(login_page.page.get_by_text(f"Logged in as {existing_user['username']}")).to_be_visible()

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
def test_invalid_user_login(login_page, users: dict):
    login_page.login(email = users["email"], password = users["password"])

    expect(login_page.page.get_by_text("Your email or password is incorrect!")).to_be_visible()

def test_empty_values_login(login_page):
    login_page.login(email = "", password = "")
    is_invalid = login_page.login_email_input.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_empty_password_login(login_page):
    login_page.login(email = "test@test.com", password = "")
    is_invalid = login_page.login_password_input.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_logout(login_page, existing_user: dict):
    login_page.login(email=existing_user["email"], password=existing_user["password"])

    expect(login_page.page.get_by_text(f"Logged in as {existing_user['username']}")).to_be_visible()

    login_page.logout()
    expect(login_page.page).to_have_url("https://automationexercise.com/login")
    expect(login_page.page.get_by_text("Login to your account")).to_be_visible()