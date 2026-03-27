from Pages.ProductsPage import ProductsPage
from playwright.sync_api import expect
import random

def test_products_page(products_page: ProductsPage):

    expect(products_page.page).to_have_url("https://automationexercise.com/products")
    expect(products_page.all_products).to_be_visible()

def test_search_random_valid_product(products_page: ProductsPage):
    product_name = products_page.search_random_product()

    expect(products_page.page.get_by_text(product_name["name"]).first).to_be_visible()
    expect(products_page.page.get_by_text(product_name["price"]).first).to_be_visible()
    expect(products_page.searched_products).to_be_visible()

def test_search_invalid_product(products_page: ProductsPage):
    products_page.search_specific_products("Some Random Product")
    assert products_page.products.count() == 0

def test_search_partial_valid_product(products_page: ProductsPage):
    search_term = random.choice(products_page.random_items)
    products_page.search_specific_products(search_term)

    # site searches across categories and tags, not just product names
    # so we only assert that results are returned, not content of results
    assert products_page.products.count() > 0

def test_empty_product_search(products_page: ProductsPage):
    products_page.search_specific_products("")
    assert products_page.products.count() == 34

def test_random_product_review_fields(products_page: ProductsPage):
    products_page.view_random_product()

    expect(products_page.review_form_name).to_be_empty()
    expect(products_page.review_form_email).to_be_empty()
    expect(products_page.review_form_text).to_be_empty()

def test_random_product_valid_review_submission(products_page: ProductsPage):
    products_page.view_random_product()
    products_page.fill_review_form("some name", "someemail@test.com", "some review!")

