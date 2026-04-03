from playwright.sync_api import Page
from Pages.ProductsPage import ProductsPage


class ProductDetailsPage(ProductsPage):

    availability_statuses = ["In Stock", "Out of Stock"]
    condition_statuses = ["New", "Used"]
    brands = ["Polo", "H&M", "Madame", "Mast & Harbour",
              "Babyhug", "Allen Solly Junior", "Kookie Kids", "Biba"]

    def __init__(self, page: Page):
        super().__init__(page)

        self.write_your_review = page.get_by_text("Write Your Review")
        self.review_form_name = page.get_by_placeholder("Your Name")
        self.review_form_email = page.get_by_placeholder("Email Address").nth(0)
        self.review_form_text = page.get_by_placeholder("Add Review Here!")
        self.submit_review_button = page.get_by_role("button", name="Submit")
        self.product_availability = page.locator("p:has(b:text('Availability:'))")
        self.product_condition = page.locator("p:has(b:text('Condition:'))")
        self.product_brand = page.locator("p:has(b:text('Brand:'))")
        self.product_quantity_box = page.locator("#quantity")
        self.product_add_to_cart = page.get_by_role("button", name=" Add To Cart")
        self.view_cart_button = page.get_by_role("link", name="View Cart")
        self.product_name = page.locator(".product-information h2")
        self.product_price = page.locator(".product-information span span")
        self.product_qty = page.locator(".disabled")
        self.product_name_cart = page.locator("h4 a")
        self.product_price_single_cart = page.locator(".cart_price p")
        self.product_price_cart = page.locator(".cart_total_price")

    def get_availability_status(self) -> str:
        return self.product_availability.text_content().replace("Availability:", "").strip()

    def get_condition_status(self) -> str:
        return self.product_condition.text_content().replace("Condition:", "").strip()

    def get_brand_name(self) -> str:
        return self.product_brand.text_content().replace("Brand:", "").strip()

    def fill_review_form(self, inputs: dict):
        self.review_form_name.fill(inputs["name"])
        self.review_form_email.fill(inputs["email"])
        self.review_form_text.fill(inputs["review"])
        self.submit_review_button.click()

    @staticmethod
    def check_availability(status) -> bool:
        return status in ProductDetailsPage.availability_statuses

    @staticmethod
    def check_condition(status) -> bool:
        return status in ProductDetailsPage.condition_statuses

    @staticmethod
    def check_brand(status) -> bool:
        return status in ProductDetailsPage.brands

    def get_product_name(self) -> str:
        return self.product_name.text_content().strip()

    def get_product_price(self) -> str:
        return self.product_price.text_content().strip()

    def add_to_cart_with_custom_quantity(self, qty: str):
        self.product_quantity_box.fill(qty)
        self.product_add_to_cart.click()
        self.view_cart_button.click()

