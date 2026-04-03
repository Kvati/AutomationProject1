from playwright.sync_api import expect, Page
from Pages.SignupPage import SignUpPage
from Pages.RegisterPage import RegisterPage
import re

card_details = {
    "name": "JohnDoe",
    "number": "1234 5678 9012 3456",
    "cvc": "123",
    "month": "12",
    "year": "2026"
}

def test_user_creation_and_item_checkout(cart_page_new_user):
    cart_page, product_count, user = cart_page_new_user

    cart_page.proceed_to_checkout_navigation()

    cart_page.verify_delivery_address(user)
    cart_page.verify_billing_address(user)

    cart_page.text_comment_frame.fill("random comment gibberish")
    cart_page.place_order_button.click()

    expect(cart_page.page).to_have_url("https://automationexercise.com/payment")

    cart_page.fill_card_details(card_details)
    cart_page.pay_and_confirm_order.click()

    expect(cart_page.page).to_have_url(re.compile(r"https://automationexercise\.com/payment_done/\d+"))
    expect(cart_page.order_placed).to_be_visible()

    download = cart_page.download_invoice()
    assert download.suggested_filename != ""

def test_checkout_register_new_user_during_checkout(cart_page_not_logged_in, register_user, page: Page):
    checkout_page, item_count = cart_page_not_logged_in

    checkout_page.proceed_to_checkout_navigation()
    checkout_page.register_login_button_navigation()

    signup_page = SignUpPage(page)
    signup_page.signup(username=register_user["username"], email=register_user["email"])

    register_page = RegisterPage(page)
    register_page.account_creation(register_user)

    register_page.continue_button.click()

    checkout_page.navigate("/view_cart")
    checkout_page.proceed_to_checkout_navigation()

    checkout_page.verify_billing_address(register_user)
    checkout_page.verify_delivery_address(register_user)

    checkout_page.text_comment_frame.fill("random comment gibberish")
    checkout_page.place_order_button.click()

    expect(checkout_page.page).to_have_url("https://automationexercise.com/payment")

    checkout_page.fill_card_details(card_details)
    checkout_page.pay_and_confirm_order.click()

    expect(checkout_page.page).to_have_url(re.compile(r"https://automationexercise\.com/payment_done/\d+"))
    expect(checkout_page.order_placed).to_be_visible()

    download = checkout_page.download_invoice()
    assert download.suggested_filename != ""