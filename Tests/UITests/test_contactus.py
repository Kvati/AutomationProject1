from playwright.sync_api import Page, expect
from Pages.ContactUsPage import ContactUsPage
import pytest


@pytest.mark.smoke
def test_contact_us_page(contact_page):
    expect(contact_page.page.get_by_role("heading", level = 2, name = "Contact Us")).to_be_visible()

@pytest.mark.regression
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

@pytest.mark.regression
def test_contact_us_form_cancel(contact_page):

    contact_page.contact_us_fill({
        "name": "JohnDoe123",
        "email": "testuser@test.com",
        "subject": "Test Subject",
        "message": "Test message"
    }, "Utils/upload_test_file.txt", accept_dialog = False)

    expect(contact_page.page.get_by_text("Success! Your details have been submitted successfully.").nth(0)).not_to_be_visible()

VALID_CONTACT = {
    "name": "John Doe",
    "email": "Test@test.com",
    "subject": "TestSubject",
    "message": "TestMessage",
}
@pytest.mark.regression
@pytest.mark.parametrize("fields, inputs", [
    pytest.param("name", {**VALID_CONTACT, "name": ""}, id="name_empty", marks=pytest.mark.xfail(reason="Known issue: No Validation for Name Field - JIRA-123")),
    pytest.param("email", {**VALID_CONTACT ,"email": ""}, id="email_empty"),
    pytest.param("subject", {**VALID_CONTACT, "subject": ""}, id="subject_empty", marks=pytest.mark.xfail(reason="Known issue: No Validation for Subject Field - JIRA-123")),
    pytest.param("message", {**VALID_CONTACT, "message": ""}, id="message_empty", marks=pytest.mark.xfail(reason="Known issue: No Validation for Message Field - JIRA-123")),
])
def test_invalid_contact_us_form(contact_page, inputs, fields):
    contact_page.contact_us_fill(inputs, "Utils/upload_test_file.txt", accept_dialog = True)

    field_locators = {
        "name": contact_page.name_field,
        "email": contact_page.email_field,
        "subject": contact_page.subject_field,
        "message": contact_page.message_field
    }

    is_invalid = field_locators[fields].evaluate("el => !el.validity.valid")
    assert is_invalid