import pytest
from playwright.sync_api import expect


def test_homepage(home_page):

    expect(home_page.feature_title_text).to_be_visible()
    expect(home_page.brands_title_text).to_be_visible()
    expect(home_page.category_title_text).to_be_visible()

def test_category_filter_visibility_women(home_page):
    home_page.expand_women_category()

    expect(home_page.women_category_tops).to_be_visible()
    expect(home_page.women_category_dress).to_be_visible()
    expect(home_page.women_category_saree).to_be_visible()

def test_category_filtering_women(home_page):
    home_page.expand_women_category()
    home_page.women_category_tops.click()
    expect(home_page.women_category_tops_title).to_be_visible()

    home_page.expand_women_category()
    home_page.women_category_dress.click()
    expect(home_page.women_category_dress_title).to_be_visible()

    home_page.expand_women_category()
    home_page.women_category_saree.click()
    expect(home_page.women_category_saree_title).to_be_visible()

def test_category_filter_visibility_men(home_page):
    home_page.expand_men_category()

    expect(home_page.men_category_jeans).to_be_visible()
    expect(home_page.men_category_t_shirts).to_be_visible()

def test_category_filtering_men(home_page):
    home_page.expand_men_category()
    home_page.men_category_jeans.click()
    expect(home_page.men_category_jeans_title).to_be_visible()

    home_page.expand_men_category()
    home_page.men_category_t_shirts.click()
    expect(home_page.men_category_t_shirts_title).to_be_visible()

def test_category_filter_visibility_kids(home_page):
    home_page.expand_kids_category()

    expect(home_page.kids_category_dress).to_be_visible()
    expect(home_page.kids_category_tops_and_shirts).to_be_visible()

def test_category_filtering_kids(home_page):
    home_page.expand_kids_category()
    home_page.kids_category_dress.click()
    expect(home_page.kids_category_dress_title).to_be_visible()

    home_page.expand_kids_category()
    home_page.kids_category_tops_and_shirts.click()
    expect(home_page.kids_category_tops_and_shirts_title).to_be_visible()

@pytest.mark.parametrize("brand, url", [
    ("Polo", "/brand_products/Polo"),
    ("H&M", "/brand_products/H&M"),
    ("Madame", "/brand_products/Madame"),
    ("Mast & Harbour", "/brand_products/Mast%20&%20Harbour"),
    ("Babyhug", "/brand_products/Babyhug"),
    ("Allen Solly Junior", "/brand_products/Allen%20Solly%20Junior"),
    ("Kookie Kids", "/brand_products/Kookie%20Kids"),
    ("Biba", "/brand_products/Biba"),
])
def test_brand_filter(home_page, brand, url):
    home_page.click_brand(brand)

    expect(home_page.page).to_have_url(f"https://automationexercise.com{url}")

def test_view_random_product(home_page):
    random_product_vars = home_page.view_random_product()

    expect(home_page.page.get_by_text(random_product_vars["name"]).first).to_be_visible()
    expect(home_page.page.get_by_text(random_product_vars["price"])).to_be_visible()

def test_add_random_product_to_cart_view_cart(home_page):
    random_product_vars = home_page.add_random_product_to_cart()

    expect(home_page.page.get_by_role("heading", name="Added!")).to_be_visible()
    expect(home_page.page.get_by_role("link", name="View Cart")).to_be_visible()

    home_page.view_cart_button.click()

    expect(home_page.page).to_have_url("https://automationexercise.com/view_cart")
    expect(home_page.page.get_by_text(random_product_vars["name"])).to_be_visible()
    expect(home_page.page.get_by_text(random_product_vars["price"]).first).to_be_visible()

def test_add_random_product_to_cart_continue_shopping(home_page):
    random_product_vars = home_page.add_random_product_to_cart()

    expect(home_page.page.get_by_role("heading", name="Added!")).to_be_visible()
    expect(home_page.page.get_by_role("link", name="View Cart")).to_be_visible()

    home_page.continue_shopping_button.click()

    expect(home_page.page).to_have_url("https://automationexercise.com/")

def test_successful_subscribe(home_page):
    #by default the field is at the bottom of the page so we need to scroll it into view
    home_page.subscribe_email_field.scroll_into_view_if_needed()

    expect(home_page.subscribe_email_field).to_be_visible()

    home_page.subscribe("SomeTest@test.com")

    expect(home_page.subscribe_success).to_be_visible()

def test_unsuccessful_subscribe(home_page):
    # by default the field is at the bottom of the page so we need to scroll it into view
    home_page.subscribe_email_field.scroll_into_view_if_needed()

    expect(home_page.subscribe_email_field).to_be_visible()

    home_page.subscribe("SomeTesttest.com")

    is_invalid = home_page.subscribe_email_field.evaluate("el => !el.validity.valid")
    assert is_invalid

def test_nav_video_tutorials_redirects_to_youtube(home_page):
    home_page.click_nav_video_tutorials()

    assert "youtube.com" in home_page.page.url