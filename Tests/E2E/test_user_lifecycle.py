import pytest
from playwright.sync_api import expect, Page
from Pages.LoginPage import LoginPage


@pytest.mark.regression
def test_register_and_delete_user(register_page, register_user: dict, page: Page):
    register_page.account_creation(register_user)

    register_page.continue_button.click()

    register_page.account_delete_button.click()

    expect(register_page.page).to_have_url("https://automationexercise.com/delete_account")
    expect(register_page.page.get_by_text("ACCOUNT DELETED!")).to_be_visible()

    register_page.continue_button.click()

    login_page = LoginPage(page)
    login_page.navigate_to_login_page()
    login_page.login(register_user["email"], register_user["password"])

    expect(login_page.page.get_by_text("Your email or password is incorrect!")).to_be_visible()