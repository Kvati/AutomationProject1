from Pages.HomePage import HomePage
from playwright.sync_api import Page
import random

class ProductsPage(HomePage):

    random_items = ["Dress", "Shirt", "Top", "Jeans"]

    def __init__(self, page: Page):
        super().__init__(page)

        self.search_input = page.get_by_placeholder("Search Product")
        self.search_button = page.locator("#submit_search")
        self.all_products =  page.get_by_role("heading", name="All Products")
        self.searched_products = page.get_by_role("heading", name="Searched Products")


    def navigate_to_products_page(self):
        self.navigate("/products")

    def search_random_product(self):
        count = self.products.count()
        random_index = random.randint(0, count - 1)
        product = self.products.nth(random_index)

        product_name = product.locator("p").text_content()
        product_price = product.locator("h2").text_content()

        self.search_input.fill(product_name)
        self.search_button.click()

        return {
            "name": product_name,
            "price": product_price
        }

    def search_specific_products(self, product_name):
        self.search_input.fill(product_name)
        self.search_button.click()
