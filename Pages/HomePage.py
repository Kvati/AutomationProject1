from Pages.BasePage import BasePage
from playwright.sync_api import Page
import random
import re



class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        #Title locators
        self.feature_title_text = page.get_by_role("heading", name="Features Items")
        self.category_title_text = page.get_by_role("heading", name="Category")
        self.brands_title_text = page.get_by_role("heading", name="Brands")

        # Women category locators
        self.women_category = page.locator("a[href='#Women']")
        self.women_category_tops = page.locator("#Women").get_by_role("link", name="Tops")
        self.women_category_saree = page.locator("#Women").get_by_role("link", name="Saree")
        self.women_category_dress = page.locator("#Women").get_by_role("link", name="Dress")
        self.women_category_tops_title = page.get_by_text("Women - Tops Products")
        self.women_category_saree_title = page.get_by_text("Women - Saree Products")
        self.women_category_dress_title = page.get_by_text("Women - Dress Products")

        #Men category locators
        self.men_category = page.locator("a[href='#Men']")
        self.men_category_t_shirts = page.locator("#Men").get_by_role("link", name="TShirts")
        self.men_category_jeans = page.locator("#Men").get_by_role("link", name="Jeans")
        self.men_category_t_shirts_title = page.get_by_text("Men - Tshirts Products")
        self.men_category_jeans_title = page.get_by_text("Men - Jeans Products")

        #Kids category locators
        self.kids_category = page.locator("a[href='#Kids']")
        self.kids_category_dress = page.locator("#Kids").get_by_role("link", name="Dress")
        self.kids_category_tops_and_shirts = page.locator("#Kids").get_by_role("link", name="Tops & Shirts")
        self.kids_category_dress_title = page.get_by_text("Kids - Dress Products")
        self.kids_category_tops_and_shirts_title = page.get_by_text("Kids - Tops & Shirts Products")

        self.products = page.locator(".productinfo")
        self.product_to_view = page.locator("a[href^='/product_details/']")

        self.view_cart_button = page.get_by_role("link", name="View Cart")
        self.continue_shopping_button = page.get_by_role("button", name = "Continue Shopping")

        self.subscribe_email_field = page.get_by_placeholder("Your email address")
        self.subscribe_button = page.locator("#subscribe")
        self.subscribe_success = page.locator(".alert-success")

        self.empty_cart_text = page.get_by_text("Cart is empty!")
        self.click_here_products_button = page.get_by_role("link", name="here")

    #amount of products on screen and view_product buttons differs,
    #due to a carousel of 6 duplicate items at the bottom of the page
    def add_random_product_to_cart(self):
        count = self.products.count()
        random_index = random.randint(0, count - 1)

        product = self.products.nth(random_index)

        product_name = product.locator("p").text_content()
        product_price = product.locator("h2").text_content()

        product.scroll_into_view_if_needed()
        product.hover()

        self.dismiss_vignette_and_retry(
            action=lambda: product.get_by_text("Add to cart").click(),
            success_condition=lambda: self.page.wait_for_selector(".modal-content", state="visible", timeout=5000)
        )

        return {
            "index": random_index,
            "name": product_name,
            "price": product_price
        }

    def view_random_product(self):
        count = self.product_to_view.count()
        random_index = random.randint(0, count - 1)

        product = self.products.nth(random_index)
        product_to_view = self.product_to_view.nth(random_index)

        product_name = product.locator("p").text_content()
        product_price = product.locator("h2").text_content()

        self.dismiss_vignette_and_retry(
            action=lambda: (product_to_view.scroll_into_view_if_needed(), product_to_view.get_by_text("View Product").click()),
            success_condition=lambda: self.page.wait_for_url(re.compile(r".*/product_details/\d+"), timeout=5000)
        )

        return {
            "index": random_index,
            "name": product_name,
            "price": product_price
        }

    def click_brand(self, brand: str):
        self.dismiss_vignette_and_retry(
            action=lambda: self.page.locator(
                f"a[href^='/brand_products/{brand}']").scroll_into_view_if_needed() or self.page.locator(
                f"a[href^='/brand_products/{brand}']").click(),
            success_condition=lambda: self.page.wait_for_url(f"**{brand}**", timeout=5000)
        )

    def expand_women_category(self):
        self.dismiss_vignette_and_retry(
            action=lambda: self.women_category.click(),
            success_condition=lambda: self.page.wait_for_selector("#Women.in", state="attached")
        )

    def expand_men_category(self):
        self.dismiss_vignette_and_retry(
            action=lambda: self.men_category.click(),
            success_condition=lambda: self.page.wait_for_selector("#Men.in", state="attached")
        )

    def expand_kids_category(self):
        self.dismiss_vignette_and_retry(
            action=lambda: self.kids_category.click(),
            success_condition=lambda: self.page.wait_for_selector("#Kids.in", state="attached")
        )

    def subscribe(self, email):
        self.subscribe_email_field.fill(email)
        self.subscribe_button.click()

    def click_here_products(self):
        self.dismiss_vignette_and_retry(
            action=lambda: self.click_here_products_button.click(),
            success_condition=lambda: self.page.wait_for_url("**/products**", timeout=5000)
        )