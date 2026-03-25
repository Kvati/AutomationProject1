from playwright.sync_api import Page
from Pages.BasePage import BasePage



class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title_mr = page.get_by_role("radio", name = "Mr.")
        self.title_mrs = page.get_by_role("radio", name = "Mrs")
        self.name = page.get_by_label("Name")
        self.email = page.get_by_label("Email")
        self.password = page.get_by_label("Password")
        self.dob_day_select = page.locator("#days")
        self.dob_month_select = page.locator("#months")
        self.dob_year_select = page.locator("#years")
        self.newsletter = page.locator("#newsletter")
        self.first_name = page.get_by_label("First Name")
        self.last_name = page.get_by_label("Last Name")
        self.company = page.get_by_label("Company", exact=True)
        self.address_1 = page.get_by_label("Address * (Street address, P.O. Box, Company name, etc.)")
        self.address_2 = page.get_by_label("Address 2")
        self.country_select = page.locator("#country")
        self.state = page.get_by_label("State")
        self.city = page.get_by_label("City")
        self.zipcode = page.locator("#zipcode")
        self.mobile_number = page.get_by_label("Mobile Number")
        self.create_account_button = page.get_by_role("button", name = "Create Account")


    def account_creation(self, user_data: dict):
        self.password.fill(user_data["password"])
        self.dob_day_select.select_option(user_data["dob_day"])
        self.dob_month_select.select_option(user_data["dob_month"])
        self.dob_year_select.select_option(user_data["dob_year"])
        self.newsletter.click()
        self.first_name.fill(user_data["first_name"])
        self.last_name.fill(user_data["last_name"])
        self.company.fill(user_data["company"])
        self.address_1.fill(user_data["address_1"])
        self.address_2.fill(user_data["address_2"])
        self.country_select.select_option(user_data["country"])
        self.state.fill(user_data["state"])
        self.city.fill(user_data["city"])
        self.zipcode.fill(user_data["zipcode"])
        self.mobile_number.fill(user_data["mobile_number"])

        self.create_account_button.click()

