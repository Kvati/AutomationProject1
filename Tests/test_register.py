from playwright.sync_api import Page,expect
from Pages.RegisterPage import RegisterPage
import pytest


def test_register_page(page: Page, random_user: dict):
    register_page = RegisterPage(page, random_user)
    expect(page.get_by_text("ENTER ACCOUNT INFORMATION")).to_be_visible()

def test_valid_user_register(page: Page, register_user: dict,random_user: dict):
    register_page = RegisterPage(page,random_user)

    register_page.account_creation(register_user)

    expect(page).to_have_url("https://automationexercise.com/account_created")
    expect(page.get_by_text("ACCOUNT CREATED!")).to_be_visible()

def test_full_empty_user_register(page: Page, empty_user: dict, random_user: dict):
    register_page = RegisterPage(page, random_user)

    register_page.account_creation(empty_user)

    password_input = page.get_by_label("Password")
    is_invalid = password_input.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_one_field_empty_user_register(page: Page, one_req_field_missing_user: dict, random_user: dict):
    register_page = RegisterPage(page, random_user)

    register_page.account_creation(one_req_field_missing_user)

    first_name = page.get_by_label("First Name")
    is_invalid = first_name.evaluate("el => !el.validity.valid")
    assert is_invalid

