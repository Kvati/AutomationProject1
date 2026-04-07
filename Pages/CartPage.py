from Pages.BasePage import BasePage
from playwright.sync_api import Page, expect
import re





class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_products = page.locator(".cart_product")
        self.empty_cart_text = page.get_by_text("Cart is empty!")
        self.click_here_products_button = page.get_by_role("link", name = "here")

        self.proceed_to_checkout = page.locator(".check_out")

        self.cart_item_delete = page.locator(".cart_quantity_delete")

        self.subscribe_email_field = page.get_by_placeholder("Your email address")
        self.subscribe_button = page.locator("#subscribe")
        self.subscribe_success = page.locator(".alert-success")

        self.your_delivery_address = page.get_by_text("Your delivery address")
        self.your_billing_address = page.get_by_text("Your billing address")

        self.delivery_first_name_last_name = page.locator("#address_delivery .address_firstname.address_lastname").nth(0)
        self.delivery_company_name = page.locator("#address_delivery .address_address1").nth(0)
        self.delivery_address_one = page.locator("#address_delivery .address_address1").nth(1)
        self.delivery_address_two = page.locator("#address_delivery .address_address1").nth(2)
        self.delivery_address_city  = page.locator("#address_delivery .address_city").nth(0)
        self.delivery_address_country_name = page.locator("#address_delivery .address_country_name").nth(0)
        self.delivery_address_phone_number = page.locator("#address_delivery .address_phone").nth(0)

        self.billing_first_name_last_name = page.locator("#address_invoice .address_firstname.address_lastname").nth(0)
        self.billing_company_name = page.locator("#address_invoice .address_address1").nth(0)
        self.billing_address_one = page.locator("#address_invoice .address_address1").nth(1)
        self.billing_address_two = page.locator("#address_invoice .address_address1").nth(2)
        self.billing_address_city = page.locator("#address_invoice .address_city").nth(0)
        self.billing_address_country_name = page.locator("#address_invoice .address_country_name").nth(0)
        self.billing_address_phone_number = page.locator("#address_invoice .address_phone").nth(0)

        self.cart_total_price = page.locator(".cart_total_price")
        self.text_comment_frame = page.locator(".form-control")
        self.register_login_button_during_checkout = page.get_by_role("link", name = "Register / Login")
        self.place_order_button = page.get_by_role("link", name = "Place Order")

        self.name_on_card = page.locator("[data-qa='name-on-card']")
        self.card_number = page.locator("[data-qa='card-number']")
        self.cvc = page.locator("[data-qa='cvc']")
        self.month_on_card = page.get_by_placeholder("MM")
        self.year_on_card = page.get_by_placeholder("YYYY")
        self.pay_and_confirm_order = page.locator("#submit")
        self.order_success = page.get_by_text("Your order has been placed successfully!")
        self.order_placed = page.locator("[data-qa='order-placed']")
        self.download_invoice_button = page.get_by_role("link", name = "Download Invoice")

    def product_deletion(self, count):
        self.cart_item_delete.nth(count).click()

    def proceed_to_checkout_navigation(self):
        self.proceed_to_checkout.click()
        self.page.wait_for_load_state("domcontentloaded")

    def register_login_button_navigation(self):
        self.register_login_button_during_checkout.click()

    def subscribe(self, email):
        self.subscribe_email_field.fill(email)
        self.subscribe_button.click()

    def total_price_check(self) -> bool:
        items = self.cart_total_price
        count = items.count()
        total = 0

        for i in range(count-1):
            total += int(items.nth(i).text_content().replace("Rs. ", "").strip())

        displayed_total = int(items.last.text_content().replace("Rs. ", "").strip())

        return total == displayed_total

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    def verify_delivery_address(self, existing_user: dict):
        delivery_city_text = self._normalize(self.delivery_address_city.text_content())

        expect(self.delivery_first_name_last_name).to_have_text(f". {existing_user['first_name']} {existing_user['last_name']}")
        expect(self.delivery_company_name).to_have_text(existing_user['company'])
        expect(self.delivery_address_one).to_have_text(existing_user['address_1'])
        expect(self.delivery_address_two).to_have_text(existing_user['address_2'])
        #assert is required here as we use _normalize to remove trailing spaces first
        assert delivery_city_text == f"{existing_user['city']} {existing_user['state']} {existing_user['zipcode']}"
        expect(self.delivery_address_country_name).to_have_text(existing_user['country'])
        expect(self.delivery_address_phone_number).to_have_text(existing_user['mobile_number'])

    def verify_billing_address(self, existing_user: dict):
        billing_city_text = self._normalize(self.billing_address_city.text_content())

        expect(self.billing_first_name_last_name).to_have_text(f". {existing_user['first_name']} {existing_user['last_name']}")
        expect(self.billing_company_name).to_have_text(existing_user['company'])
        expect(self.billing_address_one).to_have_text(existing_user['address_1'])
        expect(self.billing_address_two).to_have_text(existing_user['address_2'])
        # assert is required here as we use _normalize to remove trailing spaces first
        assert billing_city_text == f"{existing_user['city']} {existing_user['state']} {existing_user['zipcode']}"
        expect(self.billing_address_country_name).to_have_text(existing_user['country'])
        expect(self.billing_address_phone_number).to_have_text(existing_user['mobile_number'])

    def fill_card_details(self, card_details: dict):
        self.name_on_card.fill(card_details["name"])
        self.card_number.fill(card_details["number"])
        self.cvc.fill(card_details["cvc"])
        self.month_on_card.fill(card_details["month"])
        self.year_on_card.fill(card_details["year"])

    def download_invoice(self):
        with self.page.expect_download() as download_info:
            self.download_invoice_button.click()
        return download_info.value