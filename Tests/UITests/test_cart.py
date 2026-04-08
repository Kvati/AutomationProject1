from playwright.sync_api import expect
from TestData.user_test_data import VALID_CARD
import random
import pytest
import re
import allure

@pytest.mark.regression
def test_empty_cart_page(home_page):
    home_page.navigate("/view_cart")

    expect(home_page.empty_cart_text).to_be_visible()
    home_page.click_here_products()
    expect(home_page.page).to_have_url("https://automationexercise.com/products")

@pytest.mark.regression
def test_successful_subscribe(cart_page_logged_in):
    cart_page, item_count = cart_page_logged_in

    #by default the field is at the bottom of the page so we need to scroll it into view
    cart_page.subscribe_email_field.scroll_into_view_if_needed()

    expect(cart_page.subscribe_email_field).to_be_visible()

    cart_page.subscribe("SomeTest@test.com")

    expect(cart_page.subscribe_success).to_be_visible()

@pytest.mark.regression
def test_unsuccessful_subscribe(cart_page_logged_in):
    cart_page, item_count = cart_page_logged_in

    # by default the field is at the bottom of the page so we need to scroll it into view
    cart_page.subscribe_email_field.scroll_into_view_if_needed()

    expect(cart_page.subscribe_email_field).to_be_visible()

    cart_page.subscribe("SomeTesttest.com")

    is_invalid = cart_page.subscribe_email_field.evaluate("el => !el.validity.valid")
    assert is_invalid

@pytest.mark.smoke
def test_filled_cart_page(cart_page_not_logged_in):
    cart_page, item_count = cart_page_not_logged_in
    random_item = random.randint(1, item_count)

    expect(cart_page.page).to_have_url("https://automationexercise.com/view_cart")
    expect(cart_page.cart_products.nth(random_item-1)).to_be_visible()
    assert cart_page.cart_products.count() == item_count
   

@pytest.mark.regression
def test_item_deletion(cart_page_not_logged_in):
    cart_page, item_count = cart_page_not_logged_in
    random_item = random.randint(1, item_count)

    cart_page.product_deletion(random_item-1)

    expect(cart_page.cart_products).to_have_count(item_count - 1)

@pytest.mark.regression
def test_proceed_to_checkout(cart_page_logged_in):
    cart_page, item_count = cart_page_logged_in

    cart_page.proceed_to_checkout_navigation()
    assert cart_page.total_price_check()
    expect(cart_page.your_billing_address).to_be_visible()
    expect(cart_page.your_delivery_address).to_be_visible()

@pytest.mark.regression
def test_checkout_address_fields(cart_page_logged_in, existing_user):
    cart_page, item_count = cart_page_logged_in

    cart_page.proceed_to_checkout_navigation()
    cart_page.verify_billing_address(existing_user)
    cart_page.verify_delivery_address(existing_user)

@pytest.mark.regression
def test_checkout_comment_field_visible(cart_page_logged_in):
    cart_page, item_count = cart_page_logged_in

    cart_page.proceed_to_checkout_navigation()

    expect(cart_page.text_comment_frame).to_be_visible()

@pytest.mark.regression
def test_place_order_without_comment(cart_page_logged_in):
    cart_page, item_count = cart_page_logged_in

    cart_page.proceed_to_checkout_navigation()
    cart_page.place_order_button.scroll_into_view_if_needed()
    cart_page.place_order_button.click()

    expect(cart_page.page).to_have_url("https://automationexercise.com/payment")

    cart_page.fill_card_details(VALID_CARD)
    cart_page.pay_and_confirm_order.click()

    expect(cart_page.page).to_have_url(re.compile(r"https://automationexercise\.com/payment_done/\d+"))
    expect(cart_page.order_placed).to_be_visible()

@pytest.mark.smoke
def test_place_order_full_card(cart_page_logged_in, browser_name):
    cart_page, item_count = cart_page_logged_in

    cart_page.proceed_to_checkout_navigation()
    cart_page.text_comment_frame.fill("random comment gibberish")
    cart_page.place_order_button.click()

    expect(cart_page.page).to_have_url("https://automationexercise.com/payment")

    cart_page.fill_card_details(VALID_CARD)
    cart_page.pay_and_confirm_order.click()

    expect(cart_page.page).to_have_url(re.compile(r"https://automationexercise\.com/payment_done/\d+"))
    expect(cart_page.order_placed).to_be_visible()

    if browser_name == "webkit":
        pytest.skip("WebKit does not support file downloads in this environment")

    download = cart_page.download_invoice()
    assert download.suggested_filename != ""

@pytest.mark.regression
@pytest.mark.parametrize("field, card_details", [
    pytest.param("name", {**VALID_CARD, "name": ""}, id="name_empty"),
    pytest.param("number", {**VALID_CARD, "number": ""}, id="number_empty"),
    pytest.param("cvc", {**VALID_CARD, "cvc": ""}, id="cvc_empty"),
    pytest.param("month", {**VALID_CARD, "month": ""}, id="month_empty"),
    pytest.param("year", {**VALID_CARD, "year": ""}, id="year_empty"),
])
def test_place_order_empty_card(cart_page_logged_in, card_details, field):
    cart_page, item_count = cart_page_logged_in

    cart_page.proceed_to_checkout_navigation()
    cart_page.text_comment_frame.fill("random comment gibberish")
    cart_page.place_order_button.click()

    cart_page.fill_card_details(card_details)

    field_locators = {
        "name": cart_page.name_on_card,
        "number": cart_page.card_number,
        "cvc": cart_page.cvc,
        "month" : cart_page.month_on_card,
        "year": cart_page.year_on_card
    }

    cart_page.pay_and_confirm_order.click()

    is_invalid = field_locators[field].evaluate("el => !el.validity.valid")
    assert is_invalid

@pytest.mark.regression
@allure.issue("JIRA-123", "Card Input cannot handle invalid inputs")
@pytest.mark.parametrize("field, card_details", [
    pytest.param("name", {**VALID_CARD, "name": "1234"}, id="numbers_in_name", marks=pytest.mark.xfail(reason="Known issue: Card Input cannot handle invalid inputs - JIRA-123")),
    pytest.param("number", {**VALID_CARD, "number": "asdqwe"}, id="letters_in_number",marks=pytest.mark.xfail(reason="Known issue: Card Input cannot handle invalid inputs - JIRA-123")),
    pytest.param("cvc", {**VALID_CARD, "cvc": "asd"}, id="letters_in_cvc",marks=pytest.mark.xfail(reason="Known issue: Card Input cannot handle invalid inputs - JIRA-123")),
    pytest.param("month", {**VALID_CARD, "month": "DEC"}, id="letters_in_month",marks=pytest.mark.xfail(reason="Known issue: Card Input cannot handle invalid inputs - JIRA-123")),
    pytest.param("year", {**VALID_CARD, "year": "adsf"}, id="letters_in_year",marks=pytest.mark.xfail(reason="Known issue: Card Input cannot handle invalid inputs - JIRA-123")),
])
def test_place_order_invalid_inputs_card(cart_page_logged_in, card_details, field):
    cart_page, item_count = cart_page_logged_in

    cart_page.proceed_to_checkout_navigation()
    cart_page.text_comment_frame.fill("random comment gibberish")
    cart_page.place_order_button.click()

    cart_page.fill_card_details(card_details)

    field_locators = {
        "name": cart_page.name_on_card,
        "number": cart_page.card_number,
        "cvc": cart_page.cvc,
        "month": cart_page.month_on_card,
        "year": cart_page.year_on_card
    }

    cart_page.pay_and_confirm_order.click()

    is_invalid = field_locators[field].evaluate("el => el.validity.typeMismatch")
    assert is_invalid