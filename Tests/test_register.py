from playwright.sync_api import Page,expect
from Pages.RegisterPage import RegisterPage
from Pages.SignupPage import SignUpPage
import pytest


def test_register_page(register_page, page: Page, register_user: dict):

    expect(register_page.page.get_by_text("ENTER ACCOUNT INFORMATION")).to_be_visible()

def test_valid_user_register(register_page, page: Page, register_user: dict):
    register_page.account_creation(register_user)

    expect(register_page.page).to_have_url("https://automationexercise.com/account_created")
    expect(register_page.page.get_by_text("ACCOUNT CREATED!")).to_be_visible()


def test_full_empty_user_register(register_page, empty_user: dict,register_user: dict):
    register_page.account_creation(empty_user)

    is_invalid = register_page.password.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_one_field_empty_user_register(register_page, one_req_field_missing_user: dict, register_user: dict):
    register_page.account_creation(one_req_field_missing_user)

    is_invalid = register_page.first_name.evaluate("el => !el.validity.valid")
    assert is_invalid

