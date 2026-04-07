from playwright.sync_api import expect
import pytest
import re
import allure


def test_product_details_page(product_details_page):
    product_page, product = product_details_page

    expect(product_page.page).to_have_url(re.compile(r"https://automationexercise.com/product_details/\d+"))


def test_chosen_product_data(product_details_page):
    product_page, product = product_details_page

    assert product_page.check_availability(product_page.get_availability_status())
    assert product_page.check_condition(product_page.get_condition_status())
    assert product_page.check_brand(product_page.get_brand_name())

@pytest.mark.parametrize("qty",[
    pytest.param("3", id = "3 items"),
    pytest.param("5", id = "5 items"),
    pytest.param("10", id = "10 items"),
])
def test_valid_add_to_cart(product_details_page, qty):
    product_page, product = product_details_page

    product_name = product_page.product_name.text_content()
    product_price = int(product_page.product_price.text_content().replace("Rs. ", ""))

    product_page.add_to_cart_with_custom_quantity(qty)

    product_price_cart = int(product_page.product_price_cart.text_content().replace("Rs. ", ""))
    product_qty = int(product_page.product_qty.text_content())

    product_name_cart = product_page.product_name_cart.text_content()
    product_price_single_cart = int(product_page.product_price_single_cart.text_content().replace("Rs. ", ""))

    expect(product_page.page).to_have_url("https://automationexercise.com/view_cart")
    assert product_qty == int(qty)

    assert product_name == product_name_cart
    assert product_price == product_price_single_cart
    assert product_price * int(qty) == product_price_cart

@allure.issue("JIRA-123", "Quantity cannot handle invalid inputs")
@pytest.mark.parametrize("qty",[
    pytest.param("-1", id = "negative", marks=pytest.mark.xfail(reason="Known issue: Quantity cannot handle invalid inputs - JIRA-123")),
    pytest.param("0", id = "zero", marks=pytest.mark.xfail(reason="Known issue: Quantity cannot handle invalid inputs - JIRA-123")),
    pytest.param("", id = "empty", marks=pytest.mark.xfail(reason="Known issue: Quantity cannot handle invalid inputs - JIRA-123")),
])
def test_invalid_add_to_cart(product_details_page, qty):
    product_page, product = product_details_page

    product_page.add_to_cart_with_custom_quantity(qty)

    # site should reject invalid quantity and not navigate to cart or error page
    expect(product_page.page).not_to_have_url("https://automationexercise.com/view_cart")
    expect(product_page.page).not_to_have_url(re.compile(r".*500.*|.*error.*"))

VALID_USER = {
    "name": "JohnDoe",
    "email": "test@test.com",
    "review": "test"
}
def test_valid_review(product_details_page):
    product_page, product = product_details_page

    product_page.fill_review_form(VALID_USER)

    expect(product_page.successful_review).to_be_visible()

@pytest.mark.parametrize("field, inputs", [
    pytest.param("name", {**VALID_USER, "name": ""}, id="name_empty"),
    pytest.param("email", {**VALID_USER, "email": ""}, id="email_empty"),
    pytest.param("review", {**VALID_USER, "review": ""}, id="review_empty")
])
def test_invalid_write_review(product_details_page, field, inputs):
    product_page, product = product_details_page

    product_page.fill_review_form(inputs)

    field_locators = {
        "name": product_page.review_form_name,
        "email": product_page.review_form_email,
        "review": product_page.review_form_text,
    }

    is_invalid = field_locators[field].evaluate("el => !el.validity.valid")
    assert is_invalid


