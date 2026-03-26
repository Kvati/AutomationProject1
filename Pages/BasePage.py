from playwright.sync_api import Page


class BasePage:

    # Header Locators
    NAV_HOME = "a[href='/']"
    NAV_PRODUCTS = "a[href='/products/']"
    NAV_CART = "a[href='/view_cart/']"
    NAV_LOGIN = "a[href='/login']"
    NAV_TEST_CASES = "a[href='/test_cases/']"
    NAV_API_TESTING = "a[href='/api_list/']"
    NAV_VIDEO_TUTORIALS = "a[href='https://www.youtube.com/c/AutomationExercise']"
    NAV_CONTACT_US = "a[href='/contact_us/']"

    def __init__(self, page: Page):
        self.page = page

    # --- Base Utilities ---
    def navigate(self, url: str):
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def click(self, locator: str):
        self.page.locator(locator).click()

    # --- Header Actions ---
    def click_nav_home(self):
        self.click(self.NAV_HOME)

    def click_nav_products(self):
        self.click(self.NAV_PRODUCTS)

    def click_nav_cart(self):
        self.click(self.NAV_CART)

    def click_nav_login(self):
        self.click(self.NAV_LOGIN)

    def click_nav_test_cases(self):
        self.click(self.NAV_TEST_CASES)

    def click_nav_api_testing(self):
        self.click(self.NAV_API_TESTING)

    def click_nav_video_tutorials(self):
        with self.page.context.expect_page() as new_page_info:
            self.click(self.NAV_VIDEO_TUTORIALS)
        return new_page_info.value

    def click_nav_contact_us(self):
        self.click(self.NAV_CONTACT_US)

