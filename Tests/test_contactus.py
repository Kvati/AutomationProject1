from playwright.sync_api import Page, expect
from Pages.ContactUsPage import ContactUsPage
import pytest


def test_contact_us_page(contact_page):
    expect(contact_page.page.get_by_role("heading", level = 2, name = "Contact Us")).to_be_visible()

@pytest.mark.parametrize("inputs", [
    pytest.param({
        "name": "JohnDoe123",
        "email": "testuser_JohnDoe@test.com",
        "subject": "John123",
        "message": "Hi!",
    }, id = "all_fields"),
    pytest.param({
        "name": "",
        "email": "sometestemail@test.com",
        "subject": "",
        "message": "",
    }, id="only_email")
])
def test_contact_us_form_confirm(contact_page, inputs: dict):

    contact_page.contact_us_fill(inputs, "Utils/upload_test_file.txt", accept_dialog = True)

    expect(contact_page.page.get_by_text("Success! Your details have been submitted successfully.").nth(0)).to_be_visible()

def test_contact_us_form_cancel(contact_page):

    contact_page.contact_us_fill({
        "name": "JohnDoe123",
        "email": "testuser@test.com",
        "subject": "Test Subject",
        "message": "Test message"
    }, "Utils/upload_test_file.txt", accept_dialog = False)

    expect(contact_page.page.get_by_text("Success! Your details have been submitted successfully.").nth(0)).not_to_be_visible()

@pytest.mark.parametrize("inputs", [
    pytest.param({
        "name": "",
        "email": "",
        "subject": "",
        "message": "",
    },id = "all_empty"),
    pytest.param({
        "name": "JohnDoe123",
        "email": "sometestemailtest.com",
        "subject": "John123",
        "message": "Hi!",
    }, id="invalid_email"),
    pytest.param({
        "name": "JohnDoe123",
        "email": "",
        "subject": "John123",
        "message": "Hi!",
    }, id="missing_email")
])
def test_invalid_contact_us_form(contact_page, inputs: dict):
    contact_page.contact_us_fill(inputs, "Utils/upload_test_file.txt", accept_dialog = True)

    is_invalid = contact_page.email_field.evaluate("el => !el.validity.valid")
    assert is_invalid